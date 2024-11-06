import json
import pika
import logging
import uvicorn
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
import endpoints

logging.basicConfig(level=logging.INFO)

class BuyerModel(BaseModel):
    name: str
    ssn: str
    email: EmailStr
    phoneNumber: str

class BuyerRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_buyer(self, buyer_data) -> int:
        buyer_id = self._get_next_id()
        buyer_data['id'] = buyer_id
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(buyer_data) + '\n')
            logging.info(f"Created buyer: {buyer_data}")
        return buyer_id

    def _get_next_id(self) -> int:
        try:
            with open(self.file_path, 'r') as f:
                return sum(1 for _ in f) + 1
        except FileNotFoundError:
            return 1

    def get_buyer(self, buyer_id) -> dict:
        try:
            with open(self.file_path, 'r') as f:
                buyers = [json.loads(line) for line in f.readlines()]
        except FileNotFoundError:
            return None
        for buyer in buyers:
            if buyer['id'] == buyer_id:
                return {
                    "name": buyer.get("name"),
                    "ssn": buyer.get("ssn"),
                    "email": buyer.get("email"),
                    "phoneNumber": buyer.get("phoneNumber"),
                }
        return None

class BuyerSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='buyer_events', exchange_type='fanout')

    def send_buyer_event(self, buyer):
        self.channel.basic_publish(exchange='buyer_events', routing_key='', body=buyer.json())

    def __get_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=pika.PlainCredentials('guest', 'guest')))
        return connection

class Container(containers.DeclarativeContainer):
    buyer_sender_provider = providers.Singleton(
        BuyerSender
    )
    buyer_repository_provider = providers.Singleton(
        BuyerRepository
    )

def create_app():
    container = Container()
    container.wire(modules=[endpoints])
    app = FastAPI()
    app.include_router(endpoints.router)
    return app

app = create_app()

router = APIRouter()

@router.get('/buyers/{id}', status_code=200)
@inject
async def get_buyer_by_id(
    id: int,
    buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider])
):
    buyer = buyer_repository.get_buyer(id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer does not exist")
    return buyer

@router.post('/buyers', status_code=201)
@inject
async def create_buyer(buyer: BuyerModel,
                        buyer_sender: BuyerSender = Depends(Provide[Container.buyer_sender_provider]),
                        buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider])):
    buyer_id = buyer_repository.create_buyer(buyer.dict())
    buyer_sender.send_buyer(buyer)
    return {"id": buyer_id}

@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    return connection

def callback(ch, method, properties, body):
    buyer = body.decode()
    logging.info(f"Received buyer: {buyer}")

if __name__ == "__main__":
    uvicorn.run('application:app', host='0.0.0.0', port=8002, reload=True)

    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(exchange='buyer_events', exchange_type='fanout')
    queue_name = 'buyer_queue'
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='buyer_events', queue=queue_name)

    logging.info('Waiting for buyers. To exit press CTRL+C')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Stopping the consumer...")
    finally:
        channel.stop_consuming()
        connection.close()

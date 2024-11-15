import threading
import uvicorn
from fastapi import FastAPI
import endpoints  
from inventory_service import start_consuming 


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(endpoints.router)

    return app

app = create_app()

def run_rabbitmq_consumer():
    start_consuming()  

if __name__ == '__main__':
    uvicorn.run('application:app', host='0.0.0.0', port=8003, reload=True)
    consumer_thread = threading.Thread(target=run_rabbitmq_consumer)
    consumer_thread.daemon = True  
    consumer_thread.start()

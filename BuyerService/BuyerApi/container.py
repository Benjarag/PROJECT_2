   
from dependency_injector import containers, providers
import pika
from BuyerApi.buyer_repository import BuyerRepository
from BuyerApi.buyer_sender import BuyerSender

class Container(containers.DeclarativeContainer):
    # Define the configuration provider
    config = providers.Configuration()

    # RabbitMQ connection provider
    rabbit_connection = providers.Singleton(
        lambda config: pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq.host)),
        config
    )

    # RabbitMQ queue provider
    buyer_queue = providers.Singleton(
        lambda rabbit_connection: rabbit_connection().channel().queue_declare(queue='buyer_queue'),
        rabbit_connection
    )

    # Buyer repository provider
    buyer_repository_provider = providers.Factory(BuyerRepository, file_path="buyers.json")

    # Buyer sender provider
    buyer_sender_provider = providers.Factory(BuyerSender, connection=rabbit_connection)

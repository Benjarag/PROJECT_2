from dependency_injector import containers, providers
import pika
from buyer_repository import BuyerRepository
from buyer_sender import BuyerSender

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # RabbitMQ connection provider
    rabbit_connection = providers.Singleton(
        lambda: pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq.host))
    )

    # RabbitMQ queue provider
    buyer_queue = providers.Singleton(
        lambda: rabbit_connection().channel().queue_declare(queue='buyer_queue')
    )

    # Buyer repository provider
    buyer_repository_provider = providers.Factory(BuyerRepository, file_path="buyers.json")

    # Buyer sender provider
    buyer_sender_provider = providers.Factory(BuyerSender, connection=rabbit_connection)

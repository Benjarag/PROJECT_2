from dependency_injector import containers, providers
from order_repository import OrderRepository
from order_sender import OrderSender

class Container(containers.DeclarativeContainer):
    order_repository_provider = providers.Singleton(OrderRepository)
    order_sender_provider = providers.Singleton(OrderSender)

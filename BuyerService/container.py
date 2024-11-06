from dependency_injector import containers, providers

from buyer_repository import BuyerRepository
from buyer_sender import BuyerSender


class Container(containers.DeclarativeContainer):
    buyer_sender_provider = providers.Singleton(
        BuyerSender
    )

    buyer_repository_provider = providers.Singleton(
        BuyerRepository
    )
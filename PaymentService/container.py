from dependency_injector import containers, providers
from payment_repository import PaymentRepository
from payment_event_sender import PaymentSender
from payment_validator import PaymentValidator


class Container(containers.DeclarativeContainer):
    payment_validator_provider = providers.Singleton(
        PaymentValidator

    )

    payment_sender_provider = providers.Singleton(
        PaymentSender
    )

    payment_repository_provider = providers.Singleton(
        PaymentRepository
    )

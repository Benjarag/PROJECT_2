from dependency_injector import containers, providers
from buyer_repository import BuyerRepository  # Import your BuyerRepository class
from buyer_service import BuyerService  # Import your BuyerService class

class Container(containers.DeclarativeContainer):
    # Define providers for your services
    buyer_repository_provider = providers.Singleton(BuyerRepository)
    buyer_service_provider = providers.Singleton(BuyerService, repository=buyer_repository_provider)

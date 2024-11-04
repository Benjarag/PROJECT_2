# container.py
from dependency_injector import containers, providers
from merchant_repository import MerchantRepository

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    merchant_repository_provider = providers.Factory(MerchantRepository, file_path=config.merchant_file_path)

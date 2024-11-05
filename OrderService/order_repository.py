import httpx
from typing import List, Dict

class OrderRepository:
    def __init__(self, merchant_service_url: str, buyer_service_url: str):
        self.merchant_service_url = merchant_service_url
        self.buyer_service_url = buyer_service_url
        self.merchants = []
        self.buyers = []

    def load_merchants(self) -> List[Dict]:
        """Load merchants from the MerchantService."""
        response = httpx.get(f"{self.merchant_service_url}/merchants")
        if response.status_code == 200:
            self.merchants = response.json()
        else:
            self.merchants = []  # Handle error case if needed
        return self.merchants

    def load_buyers(self) -> List[Dict]:
        """Load buyers from the BuyerService."""
        response = httpx.get(f"{self.buyer_service_url}/buyers")
        if response.status_code == 200:
            self.buyers = response.json()
        else:
            self.buyers = []  # Handle error case if needed
        return self.buyers

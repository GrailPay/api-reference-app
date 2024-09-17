import random
from dto import AccountRouting
from config import Config

class AccountRoutingFactory:

    def __init__( self, config: Config ) -> None:
        self.config = config

    @staticmethod
    def generate_account_number() -> int:
        return random.randint(10 ** 11, 10 ** 12 - 1)

    def build( self ) -> AccountRouting:
        return AccountRouting(
            routing_number=self.config.ROUTING_NUMBER,
            account_number=str( AccountRoutingFactory.generate_account_number() )
        )

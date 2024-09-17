import random
from dto import AccountRouting
from config import Config

class AccountRoutingFactory:
    def __init__( self, config ):
        self.config = config

    @staticmethod
    def generate_account_number():
        return random.randint(10 ** 11, 10 ** 12 - 1)

    def build( self ):
        return AccountRouting(
            routing_number=self.config.ROUTING_NUMBER,
            account_number=str( AccountRoutingFactory.generate_account_number() )
        )

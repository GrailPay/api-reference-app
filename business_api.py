from api_base import ApiBase
from config import Config
from endpoints import Endpoints
from dto import Business
from business_builder import BusinessBuilder

class BusinessApi( ApiBase ):
    def __init__(self, config: Config):
        super().__init__(config)

    def create( self ) -> None:
        """
        This method creates and registers a business with the GrailPay API

        :return:
        """

        business: Business = (BusinessBuilder( self.config )
                              .random_email()
                              .random_tin()
                              .random_account_routing()
                              .build())

        self.api_caller.post(
            self.endpoints.get_url( Endpoints.BUSINESS_CREATE ),
            business.__dict__
        )

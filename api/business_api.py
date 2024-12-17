import logging

from api.api_base import ApiBase
from core.config import Config
from api.endpoints import Endpoints
from dto import Business
from core.business_builder import BusinessBuilder

class BusinessApi( ApiBase ):

    def __init__( self, config: Config, logger: logging.Logger ):
        super().__init__( config, logger )

    def create( self ) -> str:
        """
        This method creates and registers a business with the GrailPay API

        :return:
        """

        business: Business = ( BusinessBuilder( self.config )
                              .random_email()
                              .random_tin()
                              .random_account_routing()
                              .build())

        response = self.api_caller.post(
            self.endpoints.get_url( Endpoints.BUSINESS_CREATE ),
            business.__dict__
        )

        if response.status_code == 201:
            response_data = response.json()
            self.logger.info( f"Created business: {response_data['data']['uuid']}" )
            return response_data['data']['uuid']

        return ""

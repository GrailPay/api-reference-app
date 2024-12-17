import logging
from config import Config
from api.endpoints import Endpoints
from api.api_caller import ApiCaller

class ApiBase:

    def __init__( self, config: Config, logger: logging.Logger  ):
        self.config = config
        self.endpoints: Endpoints = Endpoints( self.config )
        self.api_caller: ApiCaller = ApiCaller( self.config, logger )
        self.logger: logging.Logger = logger

import logging
from config import Config
import requests
import json
import logging

def call_logging(func):
    """
    Decorator for adding loging to pre/post api calls.
    :param func:
    :return:
    """
    def wrapper( self, *args, **kwargs):
        self.pre_logging( *args, **kwargs)
        response = func( self, *args, **kwargs)
        self.post_logging(response)
        return response

    return wrapper

class ApiCaller:

    def __init__( self, config: Config, logger: logging.Logger ) -> None:
        self.config = config
        self.logger = logger

    def get_headers( self ) -> dict:
        """
        This method returns the headers required to authorize and correctly call APIs

        :return: dict
        """

        headers: dict = {
            "Authorization": f"Bearer {self.config.VENDOR_API_KEY}",
            "accept": "application/json",
            "content-type": "application/json"
        }

        return headers

    def pre_logging( self, url, data: dict = None ) -> None:
        self.logger.info( f"Calling {url}" )
        if data:
            self.logger.debug( f"Data: {data}" )

    def post_logging( self, response ):
        self.logger.info( f"Status Code: {response.status_code}" )

        try:
            formatted_response: str = json.dumps( response.json(), indent = 4 )
        except ValueError:
            formatted_response: str = response.text

        self.logger.debug( f"Response Body: {formatted_response}" )

    @call_logging
    def get( self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a get request.
        :param url:
        :param data:
        :return:
        """

        response: requests.Response = requests.get( url, headers = self.get_headers(), data = data )

        return response

    @call_logging
    def post( self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a post request.
        :param url:
        :param data:
        :return:
        """

        response: requests.Response = requests.post( url, headers = self.get_headers(), json = data )

        return response

    @call_logging
    def put( self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a put request.
        :param url:
        :param data:
        :return:
        """

        response: requests.Response = requests.put( url, headers = self.get_headers(), json = data )

        return response

    @call_logging
    def delete( self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a delete request.
        :param url:
        :param data:
        :return:
        """

        response: requests.Response = requests.delete( url, headers = self.get_headers(), json = data )

        return response

from config import Config
import requests
import json

class ApiCaller:
    METHOD_GET: str = "GET"
    METHOD_POST: str = "POST"
    METHOD_PUT: str = "PUT"
    METHOD_DELETE: str = "DELETE"

    def __init__( self, config: Config ) -> None:
        self.config = config

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

    def call( self, url: str, method: str, data: dict = None ) -> requests.Response | None:

        headers: dict = self.get_headers()
        response = None

        print( f"Calling {url} with method {method}" )
        if data:
            print( f"Data: {data}" )


        if method == self.METHOD_GET:
            response: requests.Response = requests.get( url, headers = headers, data = data )
        elif method == self.METHOD_POST:
            response: requests.Response = requests.post( url, headers = headers, json = data )
        elif method == self.METHOD_PUT:
            response: requests.Response = requests.put( url, headers = headers, json = data )
        elif method == self.METHOD_DELETE:
            response: requests.Response = requests.delete( url, headers = headers, json = data )

        print( f"Status Code: {response.status_code}" )
        try:
            formatted_response: str = json.dumps( response.json(), indent = 4 )
        except ValueError:
            formatted_response: str = response.text
        print( f"Response Body: {formatted_response}" )

        return response

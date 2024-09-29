from config import Config
import requests
import json

class ApiCaller:

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

    @staticmethod
    def pre_logging( method: str, url, data: dict = None ) -> None:
        print(f"Calling {method} {url}")
        if data:
            print(f"Data: {data}")

    @staticmethod
    def post_logging(response):
        print(f"Status Code: {response.status_code}")
        try:
            formatted_response: str = json.dumps(response.json(), indent=4)
        except ValueError:
            formatted_response: str = response.text
        print(f"Response Body: {formatted_response}")


    def get(self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a get request.
        :param url:
        :param data:
        :return:
        """

        self.pre_logging( "get", url, data)

        response: requests.Response = requests.get( url, headers = self.get_headers(), data = data )

        self.post_logging(response)

        return response

    def post(self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a post request.
        :param url:
        :param data:
        :return:
        """

        self.pre_logging( "post", url, data)

        response: requests.Response = requests.post(url, headers=self.get_headers(), json=data)

        self.post_logging(response)

        return response

    def put(self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a put request.
        :param url:
        :param data:
        :return:
        """

        self.pre_logging( "put", url, data)

        response: requests.Response = requests.put(url, headers=self.get_headers(), json=data)

        self.post_logging(response)

        return response

    def delete(self, url: str, data: dict = None ) -> requests.Response | None:
        """
        Makes an api call using a delete request.
        :param url:
        :param data:
        :return:
        """

        self.pre_logging( "delete", url, data)

        response: requests.Response = requests.delete(url, headers=self.get_headers(), json=data)

        self.post_logging(response)

        return response

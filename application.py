import requests
import json

from business_factory import BusinessFactory
from dto import Webhook, Business, Transaction, TransactionMid
from config import Config
from endpoints import Endpoints


class Application:
    CONFIG_FILE: str = "config.yaml"

    def __init__(self) -> None:
        self.config: Config = Config(self.CONFIG_FILE)
        self.endpoints: Endpoints = Endpoints(self.config)

    def get_headers(self) -> dict:
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

    def call_api( self, url: str, method: str, data: dict = None) -> requests.Response | None:
        """
        This method makes a call to the GrailPay API

        :param url: The API endpoint to call.
        :param method: The HTTP method to use.
        :param data: Optional data to send with the request.
        :return:
        """

        headers: dict = self.get_headers()
        response = None

        print(f"Calling {url} with method {method}")
        if data:
            print(f"Data: {data}")

        if method == "GET":
            response: requests.Response = requests.get(url, headers=headers, json=data)
        elif method == "POST":
            response: requests.Response= requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response: requests.Response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response: requests.Response = requests.delete(url, headers=headers, json=data)

        print(f"Status Code: {response.status_code}")
        try:
            formatted_response: str = json.dumps(response.json(), indent=4)
        except ValueError:
            formatted_response: str = response.text
        print(f"Response Body: {formatted_response}")

        return response

    def register_webhook(self) -> None:
        """
        This method registers a webhook with the GrailPay API

        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.WEBHOOK_REGISTER)

        webhook: Webhook = Webhook(
            webhook_url=[
                self.config.WEBHOOK_URL
            ],
            event_names=[
                "TransactionStarted",
                "TransactionCaptureStarted",
                "TransactionCompleted",
                "TransactionFailed",
                "TransactionCanceled",
                "PayoutOnHold",
                "PayoutCompleted",
                "ClawbackStarted",
                "ClawbackFailed",
                "ClawbackCompleted",
                "BankLinkedSuccessfully",
                "BankLinkFailed",
                "BusinessCreated",
                "BusinessUpdated",
                "RefundPending",
                "RefundCaptureStarted",
                "RefundCaptureCompleted",
                "RefundCaptureFailed",
                "RefundPayoutPending",
                "RefundPayoutCompleted",
                "RefundPayoutFailed",
            ]
        )

        self.call_api( url, "POST", webhook.__dict__)

    def deregister_webhook(self) -> None:
        """
        This method deregisters a webhook with the GrailPay API

        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.WEBHOOK_DEREGISTER)

        webhook: Webhook = Webhook(
            webhook_url=[
                self.config.WEBHOOK_URL
            ],
            event_names=[
                "TransactionStarted",
                "TransactionCaptureStarted",
                "TransactionCompleted",
                "TransactionFailed",
                "TransactionCanceled",
                "PayoutOnHold",
                "PayoutCompleted",
                "ClawbackStarted",
                "ClawbackFailed",
                "ClawbackCompleted",
                "BankLinkedSuccessfully",
                "BankLinkFailed",
                "BusinessCreated",
                "BusinessUpdated",
                "RefundPending",
                "RefundCaptureStarted",
                "RefundCaptureCompleted",
                "RefundCaptureFailed",
                "RefundPayoutPending",
                "RefundPayoutCompleted",
                "RefundPayoutFailed",
            ]
        )

        self.call_api(url, "DELETE", webhook.__dict__)

    def fetch_webhook(self) -> None:
        """
        This method fetches a webhook with the GrailPay API

        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.WEBHOOK_FETCH)

        self.call_api( url, "GET")

    def business_create(self) -> None:
        """
        This method creates and registers a business with the GrailPay API

        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.BUSINESS_CREATE)

        business: Business = BusinessFactory(self.config).build()

        self.call_api( url, "POST", business.__dict__)

    def transaction_create(self, payer_uuid: str, payee_uuid: str, amount: int) -> None:
        """
        This method creates a transaction with the GrailPay API using a uuid for the payer and payee

        :param payer_uuid: The uuid of the payer entity.
        :param payee_uuid: The uuid of the payee entity.
        :param amount: The amount in cents to transfer.
        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_CREATE)

        transaction: Transaction = Transaction(
            payer_uuid=payer_uuid,
            payee_uuid=payee_uuid,
            amount=amount)

        self.call_api( url, "POST", transaction.__dict__)

    def transaction_fetch(self, transaction_uuid: str) -> None:
        """
        This method fetches a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to fetch.
        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_FETCH)
        url = url.replace("{transaction_uuid}", transaction_uuid)

        self.call_api( url, "GET")

    def transaction_cancel(self, transaction_uuid: str ) -> None:
        """
        This method cancels a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to cancel.
        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_CANCEL)
        url = url.replace("{transaction_uuid}", transaction_uuid)

        self.call_api( url, "DELETE")

    def transaction_create_mid(self, payer_uuid: str, payee_mid: str, amount: int) -> None:
        """
        This method creates a transaction with the GrailPay API using a uuid for the payor and a mid for the payee

        :param payer_uuid: The uuid of the payer entity.
        :param payee_mid: The mid of the payee entity.
        :param amount: The amount in cents to transfer.
        :return:
        """

        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_CREATE)

        transaction: TransactionMid = TransactionMid(
            payer_uuid=payer_uuid,
            processor_mid=payee_mid,
            amount=amount)

        self.call_api( url, "POST", transaction.__dict__)


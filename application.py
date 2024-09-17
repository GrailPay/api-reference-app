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
        headers: dict = {
            "Authorization": f"Bearer {self.config.VENDOR_API_KEY}",
            "accept": "application/json",
            "content-type": "application/json"
        }

        return headers

    def call_api( self, url: str, method: str, data: dict = None) -> requests.Response | None:
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
        url: str = self.endpoints.get_url(Endpoints.WEBHOOK_FETCH)

        self.call_api( url, "GET")

    def business_create(self) -> None:
        url: str = self.endpoints.get_url(Endpoints.BUSINESS_CREATE)

        business: Business = BusinessFactory(self.config).build()

        self.call_api( url, "POST", business.__dict__)

    def transaction_create(self, payor_uuid, payee_uuid, amount) -> None:
        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_CREATE)

        transaction: Transaction = Transaction(
            payer_uuid=payor_uuid,
            payee_uuid=payee_uuid,
            amount=amount)

        self.call_api( url, "POST", transaction.__dict__)

    def transaction_fetch(self, transaction_uuid) -> None:
        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_FETCH)
        url = url.replace("{transaction_uuid}", transaction_uuid)

        self.call_api( url, "GET")

    def transaction_cancel(self, transaction_uuid) -> None:
        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_CANCEL)
        url = url.replace("{transaction_uuid}", transaction_uuid)

        self.call_api( url, "DELETE")

    def transaction_create_mid(self, payor_uuid, payee_mid, amount) -> None:
        url: str = self.endpoints.get_url(Endpoints.TRANSACTION_CREATE)

        transaction: TransactionMid = TransactionMid(
            payer_uuid=payor_uuid,
            processor_mid=payee_mid,
            amount=amount)

        self.call_api( url, "POST", transaction.__dict__)


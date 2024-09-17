import requests
import json
import random
import string
from dto import Webhook, Business, Transaction, TransactionMid
from config import Config
from endpoints import Endpoints
from account_routing_factory import AccountRoutingFactory


class Application:
    CONFIG_FILE = "config.yaml"

    def __init__(self):
        self.config = Config(self.CONFIG_FILE)
        self.endpoints = Endpoints(self.config)

    def get_headers(self):
        headers = {
            "Authorization": f"Bearer {self.config.VENDOR_API_KEY}",
            "accept": "application/json",
            "content-type": "application/json"
        }

        return headers

    def call_api( self, url, method, data=None):
        headers = self.get_headers()
        response = None

        print(f"Calling {url} with method {method}")
        if data:
            print(f"Data: {data}")

        if method == "GET":
            response = requests.get(url, headers=headers, json=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, json=data)

        print(f"Status Code: {response.status_code}")
        try:
            formatted_response = json.dumps(response.json(), indent=4)
        except ValueError:
            formatted_response = response.text
        print(f"Response Body: {formatted_response}")

        return response

    @staticmethod
    def generate_random_email():
        random_user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"{random_user}@test.com"
        return email

    @staticmethod
    def generate_random_tin():
        return ''.join(random.choices('0123456789', k=9))

    def register_webhook(self):
        url = self.endpoints.get_url(Endpoints.WEBHOOK_REGISTER)

        dto = Webhook(
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

        self.call_api( url, "POST", dto.__dict__)

    def deregister_webhook(self):
        url = self.endpoints.get_url(Endpoints.WEBHOOK_DEREGISTER)

        dto = Webhook(
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

        self.call_api(url, "DELETE", dto.__dict__)

    def fetch_webhook(self):
        url = self.endpoints.get_url(Endpoints.WEBHOOK_FETCH)

        self.call_api( url, "GET")

    def business_create(self):
        url = self.endpoints.get_url(Endpoints.BUSINESS_CREATE)

        random_account_routing = AccountRoutingFactory(self.config).build()
        random_tin = self.generate_random_tin()
        random_email = self.generate_random_email()

        dto = Business(
            client_reference_id = "abcd",
            kyb = self.config.KYB,
            first_name = "John",
            last_name = "Doe",
            email = random_email,
            phone = "1234567890",
            business = {
                "name": "John Incorporation",
                "tin": f"{random_tin}",
                "trading_name": "John Incorporation",
                "entity_type": "Sole Trader",
                "incorporation_date": "2024-02-02",
                "incorporation_state": "CO",
                "industry": "Nature of business",
                "industry_classification": {
                    "code_type": "SIC",
                    "codes": [
                        "NAICS 42",
                        "NAICS 45"
                    ],
                    "description": "abcdefg"
                },
                "source_of_wealth": "2344",
                "source_of_funds": "Business revenue",
                "first_transaction_completed_at": "2024-05-02 16:14:25",
                "product_type": "financial",
                "registered_as_inactive": False,
                "address_type": "Registered",
                "address": {
                    "line_1": "10554 W Quarles Ave",
                    "city": "Littleton",
                    "state": "CO",
                    "zip": "80127"
                }
            },
            business_owners = [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "dob": "2023-04-11",
                    "ssn9": "123456789",
                    "address": {
                        "line_1": "10554 W Quarles Ave",
                        "city": "Littleton",
                        "state": "CO",
                        "zip": "80127"
                    },
                    "is_beneficial_owner": True,
                    "is_director": False,
                    "is_account_owner": False,
                    "is_share_holder": False,
                    "is_significant_control_person": False,
                    "ownership_percentage": 25,
                    "email": random_email,
                    "phone": "1234567890",
                    "occupation": "Co-founder",
                    "first_transaction_completed_at": "2024-05-02 16:14:25",
                    "product_type": "financial"
                }
            ],
            bank_account = {
                "custom": {
                    "account_number": f"{random_account_routing.account_number}",
                    "routing_number": f"{random_account_routing.routing_number}",
                    "account_name": "Jack Jones",
                    "account_type": "checking"
                }
            }
        )

        self.call_api( url, "POST", dto.__dict__)

    def transaction_create(self, payor_uuid, payee_uuid, amount):
        url = self.endpoints.get_url(Endpoints.TRANSACTION_CREATE)

        transaction = Transaction(
            payer_uuid=payor_uuid,
            payee_uuid=payee_uuid,
            amount=amount)

        self.call_api( url, "POST", transaction.__dict__)

    def transaction_fetch(self, transaction_uuid):
        url = self.endpoints.get_url(Endpoints.TRANSACTION_FETCH)
        url = url.replace("{transaction_uuid}", transaction_uuid)

        self.call_api( url, "GET")

    def transaction_cancel(self, transaction_uuid):
        url = self.endpoints.get_url(Endpoints.TRANSACTION_CANCEL)
        url = url.replace("{transaction_uuid}", transaction_uuid)

        self.call_api( url, "DELETE")

    def transaction_create_mid(self, payor_uuid, payee_mid, amount):
        url = self.endpoints.get_url(Endpoints.TRANSACTION_CREATE)

        transaction = TransactionMid(
            payer_uuid=payor_uuid,
            processor_mid=payee_mid,
            amount=amount)

        self.call_api( url, "POST", transaction.__dict__)


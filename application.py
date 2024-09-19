import requests
from business_factory import BusinessFactory
from dto import Webhook, Business, Transaction, TransactionMid, TransactionList
from config import Config
from endpoints import Endpoints
from api_caller import ApiCaller


class Application:
    CONFIG_FILE: str = "config.yaml"

    def __init__( self ) -> None:
        self.config: Config = Config( self.CONFIG_FILE )
        self.endpoints: Endpoints = Endpoints( self.config )
        self.api_caller: ApiCaller = ApiCaller( self.config )

        self.webhook_events: list = [
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

    def call_api( self, url: str, method: str, data: dict = None) -> requests.Response | None:
        """
        This method makes a call to the GrailPay API

        :param url: The API endpoint to call.
        :param method: The HTTP method to use.
        :param data: Optional data to send with the request.
        :return:
        """

        return self.api_caller.call(url, method, data)

    def register_webhook( self ) -> None:
        """
        This method registers a webhook with the GrailPay API

        :return:
        """

        webhook: Webhook = Webhook(
            webhook_url = [
                self.config.WEBHOOK_URL
            ],
            event_names = self.webhook_events
        )

        self.call_api(
            self.endpoints.get_url( Endpoints.WEBHOOK_REGISTER ),
            ApiCaller.METHOD_POST,
            webhook.__dict__
        )

    def deregister_webhook( self ) -> None:
        """
        This method deregisters a webhook with the GrailPay API

        :return:
        """

        webhook: Webhook = Webhook(
            webhook_url = [
                self.config.WEBHOOK_URL
            ],
            event_names = self.webhook_events
        )

        self.call_api(
            self.endpoints.get_url( Endpoints.WEBHOOK_DEREGISTER ),
            ApiCaller.METHOD_DELETE,
            webhook.__dict__
        )

    def fetch_webhook( self ) -> None:
        """
        This method fetches a webhook with the GrailPay API

        :return:
        """

        self.call_api(
            self.endpoints.get_url( Endpoints.WEBHOOK_FETCH ),
            ApiCaller.METHOD_GET
        )

    def business_create( self ) -> None:
        """
        This method creates and registers a business with the GrailPay API

        :return:
        """

        business: Business = BusinessFactory( self.config ).build()

        self.call_api(
            self.endpoints.get_url( Endpoints.BUSINESS_CREATE ),
            ApiCaller.METHOD_POST,
            business.__dict__
        )

    def transaction_create( self, payer_uuid: str, payee_uuid: str, amount: int ) -> None:
        """
        This method creates a transaction with the GrailPay API using a uuid for the payer and payee

        :param payer_uuid: The uuid of the payer entity.
        :param payee_uuid: The uuid of the payee entity.
        :param amount: The amount in cents to transfer.
        :return:
        """

        transaction: Transaction = Transaction(
            payer_uuid = payer_uuid,
            payee_uuid = payee_uuid,
            amount = amount
        )

        self.call_api(
            self.endpoints.get_url( Endpoints.TRANSACTION_CREATE ),
            ApiCaller.METHOD_POST,
            transaction.__dict__
        )

    def transaction_fetch( self, transaction_uuid: str ) -> None:
        """
        This method fetches a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to fetch.
        :return:
        """

        url: str = self.endpoints.get_url( Endpoints.TRANSACTION_FETCH )
        url = url.replace("{transaction_uuid}", transaction_uuid )

        self.call_api( url, ApiCaller.METHOD_GET )

    def transaction_list( self ) -> None:
        """
        This method fetches a list of transactions with the GrailPay API

        :return:
        """

        transaction_list: TransactionList = TransactionList( pageSize = 200 )

        self.call_api(
            self.endpoints.get_url( Endpoints.TRANSACTION_LIST ),
            ApiCaller.METHOD_GET,
            transaction_list.__dict__
        )

    def transaction_cancel( self, transaction_uuid: str ) -> None:
        """
        This method cancels a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to cancel.
        :return:
        """

        url: str = self.endpoints.get_url( Endpoints.TRANSACTION_CANCEL )
        url = url.replace( "{transaction_uuid}", transaction_uuid )

        self.call_api( url, ApiCaller.METHOD_DELETE )

    def transaction_create_mid( self, payer_uuid: str, payee_mid: str, amount: int ) -> None:
        """
        This method creates a transaction with the GrailPay API using a uuid for the payor and a mid for the payee

        :param payer_uuid: The uuid of the payer entity.
        :param payee_mid: The mid of the payee entity.
        :param amount: The amount in cents to transfer.
        :return:
        """

        transaction: TransactionMid = TransactionMid(
            payer_uuid = payer_uuid,
            processor_mid = payee_mid,
            amount = amount
        )

        self.call_api(
            self.endpoints.get_url( Endpoints.TRANSACTION_CREATE ),
            ApiCaller.METHOD_POST,
            transaction.__dict__
        )


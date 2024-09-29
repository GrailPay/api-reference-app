from api_base import ApiBase
from config import Config
from endpoints import Endpoints
from api_caller import ApiCaller
from dto import Transaction, TransactionMid, TransactionList

class TransactionApi( ApiBase ):
    def __init__(self, config: Config):
        super().__init__(config)

        self.config = config
        self.endpoints: Endpoints = Endpoints(self.config)
        self.api_caller: ApiCaller = ApiCaller(self.config)

    def create( self, payer_uuid: str, payee_uuid: str, amount: int ) -> None:
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

        self.api_caller.post(
            self.endpoints.get_url( Endpoints.TRANSACTION_CREATE ),
            transaction.__dict__
        )

    def create_mid( self, payer_uuid: str, payee_mid: str, amount: int ) -> None:
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

        self.api_caller.post(
            self.endpoints.get_url( Endpoints.TRANSACTION_CREATE ),
            transaction.__dict__
        )

    def fetch( self, transaction_uuid: str ) -> None:
        """
        This method fetches a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to fetch.
        :return:
        """

        url: str = self.endpoints.get_url( Endpoints.TRANSACTION_FETCH )
        url = url.replace("{transaction_uuid}", transaction_uuid )

        self.api_caller.get( url )

    def list( self ) -> None:
        """
        This method fetches a list of transactions with the GrailPay API

        :return:
        """

        transaction_list: TransactionList = TransactionList( pageSize = 200 )

        self.api_caller.get(
            self.endpoints.get_url( Endpoints.TRANSACTION_LIST ),
            transaction_list.__dict__
        )

    def cancel( self, transaction_uuid: str ) -> None:
        """
        This method cancels a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to cancel.
        :return:
        """

        url: str = self.endpoints.get_url( Endpoints.TRANSACTION_CANCEL )
        url = url.replace( "{transaction_uuid}", transaction_uuid )

        self.api_caller.delete( url )

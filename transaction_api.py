import logging
from api_base import ApiBase
from config import Config
from endpoints import Endpoints
from dto import Transaction, TransactionMid, TransactionList

class TransactionApi( ApiBase ):

    def __init__( self, config: Config, logger: logging.Logger ):
        super().__init__( config, logger )

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

        response = self.api_caller.post(
            self.endpoints.get_url( Endpoints.TRANSACTION_CREATE ),
            transaction.__dict__
        )

        if response.status_code == 201:
            response_data = response.json()
            self.logger.info( f"Created transaction: {response_data['data']['uuid']}")

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

        response = self.api_caller.post(
            self.endpoints.get_url( Endpoints.TRANSACTION_CREATE ),
            transaction.__dict__
        )

        if response.status_code == 201:
            response_data = response.json()
            self.logger.info( f"Created transaction: {response_data['data']['uuid']}")

    def fetch( self, transaction_uuid: str ) -> None:
        """
        This method fetches a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to fetch.
        :return:
        """

        url: str = self.endpoints.get_url( Endpoints.TRANSACTION_FETCH )
        url = url.replace("{transaction_uuid}", transaction_uuid )

        response = self.api_caller.get( url )

        if response.status_code == 200:
            response_data = response.json()
            self.show_transaction( response_data[ 'data' ] )

    def list( self ) -> None:
        """
        This method fetches a list of transactions with the GrailPay API

        :return:
        """

        transaction_list: TransactionList = TransactionList( pageSize = 200 )

        response = self.api_caller.get(
            self.endpoints.get_url( Endpoints.TRANSACTION_LIST ),
            transaction_list.__dict__
        )

        if response.status_code == 200:
            response_data = response.json()
            for transaction in response_data[ 'data' ][ 'transactions' ]:
                self.show_transaction( transaction )

    def cancel( self, transaction_uuid: str ) -> None:
        """
        This method cancels a transaction with the GrailPay API using a transaction uuid

        :param transaction_uuid: The uuid of the transaction to cancel.
        :return:
        """

        url: str = self.endpoints.get_url( Endpoints.TRANSACTION_CANCEL )
        url = url.replace( "{transaction_uuid}", transaction_uuid )

        self.api_caller.delete( url )

    def show_transaction( self, transaction: dict ) -> None:
        self.logger.info( f"UUID: {transaction['uuid']}")
        self.logger.info( f"capture_status: {transaction['capture_status']}")
        self.logger.info( f"payout_status: {transaction['payout_status']}")
        self.logger.info( "-------------------------------" )

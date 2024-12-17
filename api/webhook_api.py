import logging
from typing import Any

from api.api_base import ApiBase
from core.config import Config
from api.endpoints import Endpoints
from dto import Webhook

class WebhookApi( ApiBase ):

    def __init__( self, config: Config, logger: logging.Logger ):
        super().__init__( config, logger )

        self.webhook_events: list = [
            "TransactionStarted",
            "TransactionCaptureStarted",
            "TransactionCompleted",
            "TransactionFailed",
            "TransactionCanceled",
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

    def register( self, webhook_url: str ) -> bool:
        """
        This method registers a webhook with the GrailPay API

        :return:
        """

        webhook: Webhook = Webhook(
            webhook_url = [
                webhook_url
            ],
            event_names = self.webhook_events
        )

        response = self.api_caller.post(
            self.endpoints.get_url( Endpoints.WEBHOOK_REGISTER ),
            webhook.__dict__
        )

        if response.status_code == 201:
            return True

        return False

    def deregister( self, webhook_url: str ) -> bool:
        """
        This method deregisters a webhook with the GrailPay API

        :return:
        """

        webhook: Webhook = Webhook(
            webhook_url = [
                webhook_url
            ],
            event_names = self.webhook_events
        )

        response = self.api_caller.delete(
            self.endpoints.get_url( Endpoints.WEBHOOK_DEREGISTER ),
            webhook.__dict__
        )

        if response.status_code == 200:
            return True

        return False

    def fetch( self ) -> dict[str, Any]:
        """
        This method fetches a webhook with the GrailPay API

        :return:
        """

        response = self.api_caller.get(
            self.endpoints.get_url( Endpoints.WEBHOOK_FETCH ),
        )

        if response.status_code == 200:
            response_data = response.json()
            for webhook in response_data[ 'data' ]:
                self.logger.info( f"Event: {webhook['event_name']} Url: {webhook['webhook_url']}" )
            return response_data

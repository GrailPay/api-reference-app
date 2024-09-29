from api_base import ApiBase
from config import Config
from endpoints import Endpoints
from dto import Webhook

class WebhookApi( ApiBase ):
    def __init__( self, config: Config ):
        super().__init__( config )

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

    def register( self ) -> None:
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

        self.api_caller.post(
            self.endpoints.get_url( Endpoints.WEBHOOK_REGISTER ),
            webhook.__dict__
        )

    def deregister( self ) -> None:
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

        self.api_caller.delete(
            self.endpoints.get_url( Endpoints.WEBHOOK_DEREGISTER ),
            webhook.__dict__
        )

    def fetch( self ) -> None:
        """
        This method fetches a webhook with the GrailPay API

        :return:
        """

        self.api_caller.get(
            self.endpoints.get_url( Endpoints.WEBHOOK_FETCH ),
        )

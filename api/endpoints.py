from core.config import Config

class Endpoints:
    WEBHOOK_REGISTER: str = "/api/v1/webhook"
    WEBHOOK_DEREGISTER: str = "/api/v1/webhook"
    WEBHOOK_FETCH: str = "/api/v1/webhook"
    BUSINESS_CREATE: str = "/api/v2/businesses"
    TRANSACTION_CREATE: str = "/api/v1/transaction"
    TRANSACTION_FETCH: str = "/api/v1/transaction/{transaction_uuid}"
    TRANSACTION_LIST: str = "/api/v2/transactions"
    TRANSACTION_CANCEL: str = "/api/v1/transaction/{transaction_uuid}"
    TRANSACTION_REFUND: str = "/api/v1/transactions/{transaction_uuid}/refund"
    TRANSACTION_FETCH_REFUNDS: str = "/api/v1/transactions/{transaction_uuid}/refunds"

    def __init__( self, config: Config ) -> None:
        self.base_url: str = "https://api-sandbox.grailpay.com/3p"

        if config.ENVIRONMENT == "production":
            self.base_url = "https://api.grailpay.com/3p"

    def get_url( self, endpoint: str ) -> str:
        """
        This method returns the full URL for an endpoint

        :param endpoint: The endpoint to get the full URL for.
        :return: str
        """

        return self.base_url + endpoint



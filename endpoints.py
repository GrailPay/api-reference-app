
class Endpoints:
    WEBHOOK_REGISTER = "/api/v1/webhook"
    WEBHOOK_DEREGISTER = "/api/v1/webhook"
    WEBHOOK_FETCH = "/api/v1/webhook"
    BUSINESS_CREATE = "/api/v2/businesses"
    TRANSACTION_CREATE = "/api/v1/transaction"
    TRANSACTION_FETCH = "/api/v1/transaction/{transaction_uuid}"
    TRANSACTION_CANCEL = "/api/v1/transaction/{transaction_uuid}"

    def __init__(self, config):
        self.base_url = "https://api-sandbox.grailpay.com/3p"

        if config.ENVIRONMENT == "production":
            self.base_url = "https://api.grailpay.com/3p"

    def get_url(self, endpoint):
        return self.base_url + endpoint



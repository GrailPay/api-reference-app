import random
import string
from core.config import Config
from dto import AccountRouting, Business
from core.account_routing_factory import AccountRoutingFactory

class BusinessBuilder:

    def __init__( self, config: Config ) -> None:
        self.config: Config = config
        self.email: str = ""
        self.tin: str = ""
        self.account_routing: AccountRouting = None

    @staticmethod
    def generate_random_email() -> str:
        """
        This method generates a random email username @test.com with 10 characters

        :return: str
        """

        random_user: str = ''.join( random.choices( string.ascii_lowercase + string.digits, k = 10 ) )
        email: str = f"{random_user}@test.com"
        return email

    @staticmethod
    def generate_random_tin() -> str:
        """
        This method generates a random 9 digit Tax Identification Number

        :return: str
        """

        return ''.join( random.choices('0123456789', k=9 ) )

    def generate_random_account_routing( self ) -> AccountRouting:
        return AccountRoutingFactory( self.config ).build()

    def random_email(self) -> 'BusinessBuilder':
        self.email: str = self.generate_random_email()
        return self

    def random_tin(self) -> 'BusinessBuilder':
        self.tin: str = self.generate_random_tin()
        return self

    def random_account_routing(self) -> 'BusinessBuilder':
        self.account_routing: AccountRouting = self.generate_random_account_routing()
        return self

    def build( self ) -> Business:
        """
        This method builds a Business object with random data

        :return: Business
        """

        business: Business = Business(
            client_reference_id = "",
            kyb = self.config.KYB,
            first_name = "John",
            last_name = "Doe",
            email = self.email,
            phone = "1234567890",
            business = {
                "name": "John Incorporation",
                "tin": f"{self.tin}",
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
                    "zip": "8012"
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
                    "email": self.email,
                    "phone": "1234567890",
                    "occupation": "Co-founder",
                    "first_transaction_completed_at": "2024-05-02 16:14:25",
                    "product_type": "financial"
                }
            ],
            bank_account = {
                "custom": {
                    "account_number": f"{self.account_routing.account_number}",
                    "routing_number": f"{self.account_routing.routing_number}",
                    "account_name": "Jack Jones",
                    "account_type": "checking"
                }
            }
        )

        return business

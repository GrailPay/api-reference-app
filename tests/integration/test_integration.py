import pytest
import logging
from config import Config
from api.webhook_api import WebhookApi
from api.business_api import BusinessApi
from transaction_api import TransactionApi

def get_log_level( level: str) -> int:
    level_map: dict = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }

    return level_map[ level.upper() ]

@pytest.fixture
def setup_and_teardown():
    # Setup logic
    print( "\nSetup" )

    CONFIG_FILE: str = "config.yaml"

    config: Config = Config( CONFIG_FILE )
    logging.basicConfig( level = get_log_level( config.LOG_LEVEL ) )
    logger = logging.getLogger( "GrailPay Test" )

    resource = ( config, logger )
    yield resource

    print("\nTeardown")

def test_webhook_register( setup_and_teardown ):
    config, logger = setup_and_teardown

    webhook_api = WebhookApi( config, logger )
    response: bool = webhook_api.register( "https://httpbin.org/post" )

    assert response is True

def test_webhook_deregister( setup_and_teardown ):
    config, logger = setup_and_teardown

    webhook_api = WebhookApi( config, logger )
    response: bool = webhook_api.deregister( "https://httpbin.org/post" )

    assert response is True

def test_webhook_fetch( setup_and_teardown ):
    config, logger = setup_and_teardown

    webhook_api = WebhookApi( config, logger )
    response: dict[ str, Any ] = webhook_api.fetch()

    assert response is not None
    assert len( response ) > 0

def test_business_create( setup_and_teardown ):
    config, logger = setup_and_teardown

    business_api = BusinessApi( config, logger )
    business_uuid: str = business_api.create()

    assert business_uuid is not None

def test_transaction_create( setup_and_teardown ):
    config, logger = setup_and_teardown

    business_api = BusinessApi( config, logger )
    payer_uuid: str = business_api.create()

    assert payer_uuid is not None

    payee_uuid: str = business_api.create()

    assert payee_uuid is not None

    transaction_api = TransactionApi( config, logger )
    transaction_uuid = transaction_api.create( payer_uuid, payee_uuid, 1000 )

    assert transaction_uuid is not None

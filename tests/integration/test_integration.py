import pytest
import logging
import json
from config import Config
from webhook_api import WebhookApi
from business_api import BusinessApi
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



import sys
import logging
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

def main() -> None:
    CONFIG_FILE: str = "config.yaml"

    config: Config = Config( CONFIG_FILE )
    logging.basicConfig( level = get_log_level( config.LOG_LEVEL ) )
    logger = logging.getLogger( "GrailPay" )

    webhook_api = WebhookApi( config, logger )
    business_api = BusinessApi( config, logger )
    transaction_api = TransactionApi( config, logger )

    actions: dict = {
        "webhook:register": ( webhook_api.register, 0, "" ),
        "webhook:deregister": ( webhook_api.deregister, 0, "" ),
        "webhook:fetch": ( webhook_api.fetch, 0, "" ),
        "business:create": ( business_api.create, 0, "" ),
        "transaction:create": ( transaction_api.create, 3, "{payer_uuid} {payee_uuid} {amount_in_cents}" ),
        "transaction:create_mid": ( transaction_api.create_mid, 3, "{payer_uuid} {payee_mid} {amount_in_cents}" ),
        "transaction:cancel": ( transaction_api.cancel, 1, "{transaction_uuid}" ),
        "transaction:fetch": ( transaction_api.fetch, 1, "{transaction_uuid}" ),
        "transaction:list": ( transaction_api.list, 0, "" ),
    }

    if len( sys.argv ) < 2:
        print( "Usage: python grailpay.py <action> [params]" )
        print( "Actions:" )
        for action, ( func, param_count, param_desc ) in actions.items():
            if param_count == 0:
                print( f"  {action}" )
            else:
                print( f"  {action} {param_desc} ")

        sys.exit( 1 )

    action = sys.argv[ 1 ]

    if action in actions:
        func, param_count, param_desc = actions[ action ]
        if len( sys.argv ) - 2 != param_count:
            print( f"Usage: python grailpay.py {action} {param_desc}" )
            sys.exit( 1 )
        params = sys.argv[ 2: ]
        func( *params )
    else:
        print( f"Unknown action: {action}" )
        sys.exit( 1 )

if __name__ == '__main__':
    main()

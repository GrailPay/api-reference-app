import sys
from application import Application

def main() -> None:
    app = Application()

    actions: dict = {
        "webhook:register": (app.register_webhook, 0, ""),
        "webhook:deregister": (app.deregister_webhook, 0, ""),
        "webhook:fetch": (app.fetch_webhook, 0, ""),
        "business:create": (app.business_create, 0, ""),
        "transaction:create": (app.transaction_create, 3, "{payer_uuid} {payee_uuid} {amount_in_cents}"),
        "transaction:create_mid": (app.transaction_create_mid, 3, "{payer_uuid} {payee_mid} {amount_in_cents}"),
        "transaction:cancel": (app.transaction_cancel, 1, "{transaction_uuid}"),
        "transaction:fetch": (app.transaction_fetch, 1, "{transaction_uuid}"),
    }

    if len( sys.argv ) < 2:
        print( "Usage: python grailpay.py <action> [params]" )
        print( "Actions:")
        for action, (func, param_count, param_desc) in actions.items():
            if param_count == 0:
                print(f"  {action}")
            else:
                print(f"  {action} {param_desc}")
        sys.exit(1)

    action = sys.argv[1]

    if action in actions:
        func, param_count, param_desc = actions[action]
        if len(sys.argv) - 2 != param_count:
            print(f"Usage: python grailpay.py {action} {param_desc}")
            sys.exit(1)
        params = sys.argv[2:]
        func(*params)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()

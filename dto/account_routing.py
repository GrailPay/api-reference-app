# dto/webhook.py

from dataclasses import dataclass

@dataclass
class AccountRouting:
    account_number: str
    routing_number: str


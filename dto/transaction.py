# dto/transaction.py

from dataclasses import dataclass, field

@dataclass
class Transaction:
    payer_uuid: str
    payee_uuid: str
    amount: int

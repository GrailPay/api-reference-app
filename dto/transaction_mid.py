# dto/transaction.py

from dataclasses import dataclass, field

@dataclass
class TransactionMid:
    payer_uuid: str
    processor_mid: str
    amount: int

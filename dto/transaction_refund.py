# dto/transaction_refund.py

from dataclasses import dataclass, field

@dataclass
class TransactionRefund:
    client_reference_id: str
    amount: int

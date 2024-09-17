# dto/business.py

from dataclasses import dataclass

@dataclass
class Business:
    client_reference_id: str
    kyb: bool
    first_name: str
    last_name: str
    email: str
    phone: str
    business: dict
    business_owners: list
    bank_account: dict

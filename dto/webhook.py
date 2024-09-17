# dto/webhook.py

from dataclasses import dataclass

@dataclass
class Webhook:
    webhook_url: list
    event_names: list


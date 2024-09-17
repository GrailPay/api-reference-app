import yaml
import os
from datetime import datetime, time as dttime


class Config:
    ENVIRONMENT: str = "sandbox"
    PROCESSOR_API_KEY: str = ""
    VENDOR_API_KEY: str = ""
    WEBHOOK_URL: str = ""
    KYB: bool = False
    ROUTING_NUMBER: str = ""

    def __init__(self, file: str) -> None:
        self.CONFIG_FILE = file
        self.load()

    def load(self) -> None:
        """
        This method loads the configuration file

        :return:
        """

        try:
            with open(self.CONFIG_FILE, "r") as f:
                config = yaml.safe_load(f)

            self.ENVIRONMENT = config["environment"]
            self.PROCESSOR_API_KEY = config["authentication"]["processor_api_key"]
            self.VENDOR_API_KEY = config["authentication"]["vendor_api_key"]
            self.WEBHOOK_URL = config["webhook"]["url"]
            self.KYB = config["onboarding"]["kyb"]
            self.ROUTING_NUMBER = config["routing_number"]

            print("Loaded config file.")

        except Exception as e:
            print( "Error loading config file. Key: " + str(e) )

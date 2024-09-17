import yaml
import os
from datetime import datetime, time as dttime


class Config:
    ENVIRONMENT = "sandbox"
    PROCESSOR_API_KEY = ""
    VENDOR_API_KEY = ""
    TEST_MID = ""
    WEBHOOK_URL = ""
    KYB = False
    ROUTING_NUMBER = ""

    def __init__(self, file):
        self.CONFIG_FILE = file
        self.load()

    def load(self):

        try:
            with open(self.CONFIG_FILE, "r") as f:
                config = yaml.safe_load(f)

            self.ENVIRONMENT = config["environment"]
            self.PROCESSOR_API_KEY = config["authentication"]["processor_api_key"]
            self.VENDOR_API_KEY = config["authentication"]["vendor_api_key"]
            self.TEST_MID = config["test_mid"]
            self.WEBHOOK_URL = config["webhook"]["url"]
            self.KYB = config["onboarding"]["kyb"]
            self.ROUTING_NUMBER = config["routing_number"]

            print("Loaded config file.")

        except Exception as e:
            print( "Error loading config file. Key: " + str(e) )
            print("Failed to load config, using defaults")

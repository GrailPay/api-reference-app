# GrailPay API Reference Application

# Purpose

This program is a reference implementation of the GrailPay API. It demonstrates how to:

* Register a webhook.
* Deregister a webhook.
* Fetch webhooks.
* Onboard a business.
* Create an ACH payment.
* Cancel an ACH payment.
* Fetch the details of an ACH payment.


# Installation
## Install Python Packages
    pip install -r requirements.txt

## Setup Config File
    cp config.yaml.example config.yaml

# Configuration

The configuration is stored in config.yaml.

## Authentication

* processor_api_key: refer to your GrailPay onboarding documentation.

* vendor_api_key: refer to your GrailPay onboarding documentation.

## Webhook

* url: The URL to receive webhook notifications.


This must be a functional URL that can receive POST requests in order for register to work correctly as it is called during the register process.

## onboarding

* kyb: bool

Only set to false if your account is configured for external KYB.
You will not be able to perform transactions unless either the payer or payee has passed a KYB check.

* routing_number: the test routing number used when creating a business. 

The account number is randomly generated.

# Usage

    python grailpay.py <action> [params]
    
## Actions

### webhook:register

    python grailpay.py webhook:register

### webhook:deregister

    python grailpay.py webhook:deregister

### webhook:fetch
    
    python grailpay.py webhook:fetch

### business:create
    
    python grailpay.py business:create

### transaction:create
    python grailpay.py transaction:create {payer_business_uuid} {payee_business_uuid} {amount}

* payer_business_uuid: The uuid of the source business.
* payee_business_uuid: The uuid of the destination business.
* amount: The amount of the transaction in cents.

### transaction:create_mid
    
    python grailpay.py transaction:create_mid payer_business_uuid payee_business_mid amount

* payer_business_uuid: The uuid of the source business.
* payee_business_mid: The mid of the destination business.
* amount: The amount of the transaction in cents.


### transaction:cancel
        
    python grailpay.py transaction:cancel {transaction_uuid}

* transaction_uuid: The uuid of the transaction to cancel.

### transaction:fetch
            
    python grailpay.py transaction:fetch {transaction_uuid}

* transaction_uuid: The uuid of the transaction to fetch.




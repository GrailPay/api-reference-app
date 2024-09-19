# GrailPay API Reference Application

Company Website: (https://grailpay.com)

API Documentation Website: (https://docs.grailpay.com)

# Purpose

This program is a reference implementation of the GrailPay API. It demonstrates how to:

* Register a webhook.
* Deregister a webhook.
* Fetch webhooks.
* Onboard a business.
* Create an ACH payment.
* Cancel an ACH payment.
* Fetch the details of a single ACH payment.
* Fetch a list of ACH payments.


# Installation

This project was developed using Python 3.12.6

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

For test purposes, sites like [webhook.site](https://webhook.site) can be used to receive webhook notifications.

## onboarding

* kyb: bool

Only set to false if your account is configured for external KYB.
You will not be able to perform transactions unless either the payer or payee has passed a KYB check.

* routing_number: the test routing number used when creating a business. 

The account number is randomly generated.

# Commands

    python grailpay.py <action> [params]
    
## Actions

### webhook:register

(https://docs.grailpay.com/docs/register-a-webhook)

    python grailpay.py webhook:register

Register the webhook url specified in the config file to receive webhook event notifications.
Currently subscribes to all events.

### webhook:deregister

(https://docs.grailpay.com/docs/deregister-webhook)

    python grailpay.py webhook:deregister

Deregister the webhook url specified in the config file to stop receiving webhook event notifications.

### webhook:fetch

(https://docs.grailpay.com/docs/fetch-webhooks)

    python grailpay.py webhook:fetch

Fetch a list of all webhooks and subscribed events.

### business:create

(https://docs.grailpay.com/v2.0/docs/onboarding-a-business)

** Note: this uses the 2.0 version of the API as the 1.0 version is being deprecated.

    python grailpay.py business:create

Create a business with a random account number and the routing number specified in the config file.
TIN and email are randomly generated.

The uuid of this entity is used in the transaction:create command. You will need to create two businesses to perform a transaction.

### transaction:create

(https://docs.grailpay.com/docs/creating-a-transaction)

    python grailpay.py transaction:create {payer_business_uuid} {payee_business_uuid} {amount}

* payer_business_uuid: The uuid of the source business.
* payee_business_uuid: The uuid of the destination business.
* amount: The amount of the transaction in cents.

Using the uuids of the businesses created in the business:create command, create a transaction between the two businesses.

### transaction:create_mid

(https://docs.grailpay.com/docs/creating-a-transaction)
    
    python grailpay.py transaction:create_mid {payer_business_uuid} {payee_business_mid} {amount}

* payer_business_uuid: The uuid of the source business.
* payee_business_mid: The mid of the destination business.
* amount: The amount of the transaction in cents.

Using the uuid of the source business and the mid of the destination business, create a transaction between the two businesses.

### transaction:cancel

(https://docs.grailpay.com/docs/cancel-transaction)

    python grailpay.py transaction:cancel {transaction_uuid}

* transaction_uuid: The uuid of the transaction to cancel.

Cancel a transaction using the uuid of the transaction.

### transaction:fetch

(https://docs.grailpay.com/docs/fetch-transaction)

    python grailpay.py transaction:fetch {transaction_uuid}

* transaction_uuid: The uuid of the transaction to fetch.

Fetch the details of a transaction using the uuid of the transaction.

### transaction:list

(https://docs.grailpay.com/v2.0/docs/fetch-transaction-list)

    python grailpay.py transaction:list

Fetch the details of the last 200 transactions.

# Usage

1. Register a webhook.

    ```
    python grailpay.py webhook:register
    ```
   
2. Create two businesses.

    ```
    python grailpay.py business:create
    python grailpay.py business:create
    ```

   * After executing the above commands, you will see the uuids of the businesses created. 
   * Use these uuids in the next step.


3. Create a transaction between the two businesses.

    ```
    python grailpay.py transaction:create {payer_business_uuid} {payee_business_uuid} {amount}
    ```
   * Replace {payer_business_uuid} and {payee_business_uuid} with the uuids of the businesses created in the previous step. 
   * Replace {amount} with the amount of the transaction in cents.


4. Fetch the details of the transaction.

    ```
    python grailpay.py transaction:fetch {transaction_uuid}
    ```
   * Replace {transaction_uuid} with the uuid of the transaction created in the previous step to see the details of the transaction.


5. Observe the webhook notifications.

    * Check the log of your webhook url to see the transaction event notifications.

    * You can read about the events here: [GrailPay Webhooks](https://docs.grailpay.com/docs/webhooks)

from paytring.constant.url import URL
from paytring.resources.paytring import Paytring
from paytring.utility.utility import Utility
import requests
import base64
import json


class Order(Paytring):

    def __init__(self):
        super().__init__()
        self.order_create_url = URL.ORDER_CREATE
        self.order_fetch_url = URL.FETCH_ORDER
        self.order_fetch_by_receipt_url = URL.FETCH_ORDER_BY_RECIEPT
        self.refund_url = URL.REFUND
        self.create_seamless_order_url = URL.ORDER_CREATE_SEAMLESS
        self.validate_vpa_url = URL.VALIDATE_VPA
        self.validate_card_url = URL.VALIDATE_CARD
        self.utility_obj = Utility()

    def create(self, receipt_id, callback_url, payment_info, customer_info, billing_info=None, shipping_info=None, notes=None, tpv=None, pg=None, pg_pool_id=None):
        """
        Use to create an Order on Paytring

        Args(type=string):
            'receipt' : Receipt Id for the order
            'callback_url' : The URL where the PAYTRING will send success/failed etc. response.

        Args(type=array):
            'payment_info' : Info about payment details like currency and amount.
            'customer_info' : Info about Customer
            'billing_info' : customer billing address
            'shipping_info' : customer shipping address
            'notes' : notes of udf fields

        Returns:
            Order Dict created for given reciept ID
        """
        try:
            self.utility_obj.validate_receipt(receipt_id)
            self.utility_obj.validate_callback_url(callback_url)
            self.utility_obj.validate_amount(payment_info['amount'])
            self.utility_obj.validate_currency(
                payment_info['currency'].upper())
            self.utility_obj.vaidate_customer_info(customer_info)
            self.utility_obj.validate_email(customer_info['email'])
            self.utility_obj.validate_phone(customer_info['phone'])

            payload = {
                "key": self.key,
                "receipt_id": receipt_id,
                "amount": payment_info['amount'],
                "callback_url": callback_url,
                "cname": customer_info['cname'],
                "email": customer_info['email'],
                "phone": customer_info['phone'],
                "currency": payment_info['currency'],
            }

            if billing_info is not None:

                billing_address = {
                    'firstname': billing_info['firstname'] if billing_info['firstname'] else None,
                    'lastname': billing_info['lastname'] if billing_info['lastname'] else None,
                    'phone': billing_info['phone'] if billing_info['phone'] else None,
                    'line1': billing_info['line1'] if billing_info['line1'] else None,
                    'line2': billing_info['line2'] if billing_info['line2'] else None,
                    'city': billing_info['city'] if billing_info['city'] else None,
                    'state': billing_info['state'] if billing_info['state'] else None,
                    'country': billing_info['country'] if billing_info['country'] else None,
                    'zipcode': billing_info['zipcode'] if billing_info['zipcode'] else None,
                }
                payload["billing_address"] = billing_address

            if shipping_info is not None:

                shipping_address = {
                    'firstname': shipping_info['firstname'] if shipping_info['firstname'] else None,
                    'lastname': shipping_info['lastname'] if shipping_info['lastname'] else None,
                    'phone': shipping_info['phone'] if shipping_info['phone'] else None,
                    'line1': shipping_info['line1'] if shipping_info['line1'] else None,
                    'line2': shipping_info['line2'] if shipping_info['line2'] else None,
                    'city': shipping_info['city'] if shipping_info['city'] else None,
                    'state': shipping_info['state'] if shipping_info['state'] else None,
                    'country': shipping_info['country'] if shipping_info['country'] else None,
                    'zipcode': shipping_info['zipcode'] if shipping_info['zipcode'] else None,
                }

                payload["shipping_address"] = shipping_address

            if notes is not None:

                notes = {
                    'udf1': notes['udf1'] if notes['udf1'] else None,
                    'udf2': notes['udf2'] if notes['udf2'] else None,
                    'udf3': notes['udf3'] if notes['udf3'] else None,
                }
                payload["notes"] = notes

            if pg is not None:
                self.utility_obj.validate_pg(pg)
                payload['pg'] = pg

            if pg_pool_id is not None:
                self.utility_obj.validate_pg_pool_id(pg_pool_id)
                payload['pg_pool_id'] = pg_pool_id

            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.order_create_url, json=payload)
            response = response.json()
            if response['status'] == True:
                if 'url' in response.keys():
                    response['url'] = base64.b64decode(
                        response['url']).decode('utf-8')
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def fetch(self, order_id):
        """
        Use to fetch an Order on Paytring throu

        Args: 
            order_id : Id for which order object has to be retrieved

        Returns:
            Order Dict for given order_id
        """
        try:
            self.utility_obj.validate_order(order_id)

            payload = {
                "key": self.key,
                "id": order_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.order_fetch_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def fetch_by_receipt_id(self, receipt_id):
        """
        Use to fetch an Order on Paytring by receipt-id

        Args: 
            receipt_id : Id for which order object has to be retrieved

        Returns:
            Order Dict for given receipt_id
        """

        try:
            self.utility_obj.validate_receipt(receipt_id)

            payload = {
                "key": self.key,
                "id": receipt_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(
                self.order_fetch_by_receipt_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def refund(self, order_id):
        """
        Use to intaite refund on Paytring by order-id

        Args: 
            order_id : Id for which refund is to be intiated

        Returns:
            Dict containing 'status' and 'message'
        """

        try:
            payload = {
                "key": self.key,
                "id": order_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.refund_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def process_order(self, order_id, method, code, vpa=None, card=None, device=None):
        """
        Used to process transaction without opening paytring checkout , also known as seamless api or custom checkout api

        Args(type=string):
            'order_id' : Order Id for the order created on Paytring
            'method' : Which method to be used for payment, eg. upi, nb, card, wallet, emi
            'code' : This parameter's value changes depending on what method it is, in case of upi you have three options collect, qr, intent.
            *'vpa' : VPA of the customer.(Only required if method is upi and code is collect)
            *'device' : Infomartion about the device OS.(mandatory if method is upi and code is intent, eg. android, ios)
        Args(type=array):
            *'card' : Infomartion about customer card.(Only required if method is card)

        """

        try:

            self.utility_obj.validate_order(order_id)
            self.utility_obj.validate_method(method)
            self.utility_obj.validate_code(code)

            payload = {
                "key": self.key,
                "order_id": order_id,
                "method": method,
                "code": code
            }

            if method == "upi" and code == "collect":
                if vpa is None:
                    raise Exception("VPA info is mandatory")
                self.utility_obj.validate_vpa(vpa)
                payload["vpa"] = vpa

            if method == 'card':
                if card is None:
                    raise Exception("Please pass card info in card argument")
                self.utility_obj.validate_card(card)
                payload["card"] = card

            if method == 'upi' and code == 'intent':
                if device is None:
                    raise Exception(
                        "Device Info is mandatory, eg. android,ios")
                self.utility_obj.validate_device(device)
                payload["device"] = device

            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(
                self.create_seamless_order_url, json=payload)
            response = response.json()
            if response['status'] == True:
                if 'url' in response.keys():
                    response['url'] = base64.b64decode(
                        response['url']).decode('utf-8')
                return {"response": response}
            return {"response": response}

        except Exception as e:

            return {"response": str(e)}

    def validate_vpa(self, vpa):
        """
        Use by merchants integrating order process api and want to check if customer provided vpa is valid or not.

        Args :
            vpa(string) : vpa you want to be validated.

        Returns :

            Dict having info whether a vpa is valid or not 
        """
        try:
            self.utility_obj.validate_vpa(vpa)

            payload = {
                "key": self.key,
                "vpa": vpa
            }

            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.validate_vpa_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}

        except Exception as e:
            return {"response": str(e)}

    def validate_card(self, bin):
        """
        Use by merchants integrating order process api and want to check if customer provided card is valid or not.

        Args :
            bin(string) :  card bin you want to be validated.( first 6 digits of card number )

        Returns :
            Dict having info whether a card is valid or not 

        """
        try:
            self.utility_obj.validate_bin(bin)

            payload = {
                "key": self.key,
                "bin": bin
            }

            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.validate_card_url, json=payload)
            print(f"paytring response : {response}")
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}

        except Exception as e:
            return {"response": str(e)}


class Subscription(Paytring):

    def __init__(self):
        super().__init__()
        self.plan_create_url = URL.PLAN_CREATE
        self.plan_fetch_url = URL.PLAN_FETCH
        self.plan_fetch_by_receipt_url = URL.PLAN_FETCH_BY_RECIEPT
        self.subscription_create_url = URL.SUBSCRIPTION_CREATE
        self.subscription_fetch_url = URL.SUBSCRIPTION_FETCH
        self.subscription_fetch_by_receipt_url = URL.SUBSCRIPTION_FETCH_BY_RECIEPT
        self.utility_obj = Utility()

    def create_plan(self, receipt_id, payment_info, plan_info, notes=None):
        """
        Use to create_plan an subscription on Paytring

        Args(type=string):
            'receipt' : Receipt Id for the plan 

        Args(type=array):
            'payment_info' : Info about payment details like currency and amount.
            'plan_info' : Info about plan title, description, frequency, cycle.
            'notes' : notes of udf fields 

        Returns:
            Plan Dict created for given plan ID
        """
        try:
            self.utility_obj.validate_receipt(receipt_id)
            self.utility_obj.validate_amount(payment_info['amount'])
            self.utility_obj.validate_currency(
                payment_info['currency'].upper())
            self.utility_obj.validate_plan_title(plan_info['title'])
            self.utility_obj.validate_plan_frequency(plan_info['frequency'])

            payload = {
                "key": self.key,
                "mer_reference_id": receipt_id,
                "amount": payment_info['amount'],
                "currency": payment_info['currency'] if payment_info['currency'] else 'INR',
                "title": plan_info['title'],
                "description": plan_info['description'] if plan_info['description'] else None,
                "frequency": plan_info['frequency'],
                "cycle": plan_info['cycle'] if plan_info['cycle'] else '12',
                "notes": {
                    "udf1": notes['udf1'] if notes['udf1'] else None,
                    "udf2": notes['udf2'] if notes['udf2'] else None,
                    "udf3": notes['udf3'] if notes['udf3'] else None
                }
            }

            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.plan_create_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def fetch_plan(self, plan_id):
        """
        Use to fetch an plan on Paytring throu

        Args: 
            plan_id : Id for which plan object has to be retrieved

        Returns:
            plan Dict for given plan_id
        """
        try:
            self.utility_obj.validate_plan_id(plan_id)

            payload = {
                "key": self.key,
                "id": plan_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.plan_fetch_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def fetch_plan_by_receipt_id(self, receipt_id):
        """
        Use to fetch an Plan on Paytring by receipt-id

        Args: 
            receipt_id : Id for which Plan object has to be retrieved

        Returns:
            Order Dict for given receipt_id
        """

        try:
            self.utility_obj.validate_receipt(receipt_id)

            payload = {
                "key": self.key,
                "id": receipt_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash

            response = requests.post(
                self.plan_fetch_by_receipt_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def create_subscription(self, receipt_id, plan_id, callback_url, customer_info, billing_info=None, shipping_info=None, notes=None, pg=None, pg_pool_id=None):
        """
        Use to create_subscription an subscription on Paytring

        Args(type=string):
            'receipt' : Receipt Id for the plan 
            'plan_id' : The unique identifier of a plan that should be linked to the Subscription
            'callback_url' : The URL where the PAYTRING will send success/failed etc. response.

        Args(type=array):
            'customer_info' : Info about Customer
            'billing_info' : customer billing address
            'shipping_info' : customer shipping address
            'notes' : notes of udf fields

        Returns:
            subscription Dict created for given subscription ID
        """
        try:
            self.utility_obj.validate_receipt(receipt_id)
            self.utility_obj.validate_plan_id(plan_id)
            self.utility_obj.validate_callback_url(callback_url)
            self.utility_obj.vaidate_customer_info(customer_info)
            self.utility_obj.validate_email(customer_info['email'])
            self.utility_obj.validate_phone(customer_info['phone'])

            payload = {
                "key": self.key,
                "mer_reference_id": receipt_id,
                "plan_id": plan_id,
                "callback_url": callback_url,
                "cname": customer_info['cname'],
                "email": customer_info['email'],
                "phone": customer_info['phone'],
                "billing_address": {
                    'firstname': billing_info['firstname'] if billing_info['firstname'] else None,
                    'lastname': billing_info['lastname'] if billing_info['lastname'] else None,
                    'phone': billing_info['phone'] if billing_info['phone'] else None,
                    'line1': billing_info['line1'] if billing_info['line1'] else None,
                    'line2': billing_info['line2'] if billing_info['line2'] else None,
                    'city': billing_info['city'] if billing_info['city'] else None,
                    'state': billing_info['state'] if billing_info['state'] else None,
                    'country': billing_info['country'] if billing_info['country'] else None,
                    'zipcode': billing_info['zipcode'] if billing_info['zipcode'] else None,
                },
                "shipping_address": {
                    'firstname': shipping_info['firstname'] if shipping_info['firstname'] else None,
                    'lastname': shipping_info['lastname'] if shipping_info['lastname'] else None,
                    'phone': shipping_info['phone'] if shipping_info['phone'] else None,
                    'line1': shipping_info['line1'] if shipping_info['line1'] else None,
                    'line2': shipping_info['line2'] if shipping_info['line2'] else None,
                    'city': shipping_info['city'] if shipping_info['city'] else None,
                    'state': shipping_info['state'] if shipping_info['state'] else None,
                    'country': shipping_info['country'] if shipping_info['country'] else None,
                    'zipcode': shipping_info['zipcode'] if shipping_info['zipcode'] else None,
                },
                "notes": {
                    'udf1': notes['udf1'] if notes['udf1'] else None,
                    'udf2': notes['udf2'] if notes['udf2'] else None,
                    'udf3': notes['udf3'] if notes['udf3'] else None,
                }
            }

            if pg is not None:
                self.utility_obj.validate_pg(pg)
                payload['pg'] = pg
            else:
                payload['pg'] = "paytring"

            if pg_pool_id is not None:
                self.utility_obj.validate_pg_pool_id(pg_pool_id)
                payload['pg_pool_id'] = pg_pool_id

            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash

            response = requests.post(
                self.subscription_create_url, json=payload)
            response = response.json()
            if response['status'] == True:
                if 'url' in response.keys():
                    response['url'] = base64.b64decode(
                        response['url']).decode('utf-8')
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def fetch_subscription(self, subscription_id):
        """
        Use to fetch an subscription on Paytring throu

        Args: 
            subscription_id : Id for which subscription object has to be retrieved

        Returns:
            Subscription Dict for given subscription_id
        """
        try:
            self.utility_obj.validate_subscription_id(subscription_id)

            payload = {
                "key": self.key,
                "id": subscription_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.subscription_fetch_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}

    def fetch_subscription_by_receipt_id(self, receipt_id):
        """
        Use to fetch an subscription on Paytring by receipt-id

        Args: 
            receipt_id : Id for which subscription object has to be retrieved

        Returns:
            Subscription Dict for given receipt_id
        """

        try:
            self.utility_obj.validate_receipt(receipt_id)

            payload = {
                "key": self.key,
                "id": receipt_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(
                self.subscription_fetch_by_receipt_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}


class CurrencyConversion(Paytring):

    def __init__(self) -> None:
        super().__init__()
        self.currency_conversion_url = URL.CURRENY_CONVERSION
        self.utility_obj = Utility()

    def convert_currency(self, currency_from, currency_to):
        """
        Use to give the latest currency conversion rate to desired currency for a given currency

        Args:
            currency_from : Base currency you want conversion to happen from
            currency_to : Final currency you want conversion to happen to

        Returns:
            Dict with converted currency details
        """
        try:

            self.utility_obj.validate_currency(currency_from)
            self.utility_obj.validate_currency(currency_to)

            payload = {
                "key": self.key,
                "from": currency_from,
                "to": currency_to
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(
                self.currency_conversion_url, json=payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}

        except Exception as e:
            return {"response": str(e)}

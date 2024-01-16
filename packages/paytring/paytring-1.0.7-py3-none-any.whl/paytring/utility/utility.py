import hashlib
import re
from datetime import datetime
from paytring.resources import Paytring

class Utility(Paytring):
    
    
    def create_hash(self, body):
    
        """Create hash for given body and key"""
        try:
            if len(body.keys()) != 0:
                keys = sorted(body.keys())
                values = [str(body[key]) for key in keys if not isinstance(body[key], dict)]
                values = '|'.join(values) + '|'
                values += self.secret
                return hashlib.sha512(values.encode('utf-8')).hexdigest()
            else:
                raise Exception('Invalid Payload')
        except Exception as e:
            raise Exception(str(e))

    def validate_email(self, email) -> bool:
        if not isinstance(email, str):
            raise Exception('Invalid email')
        
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        raise Exception('Invalid email')

    def validate_amount(self, amount) -> bool:
        if not isinstance(amount, str):
            raise Exception('Invalid amount')
        
        if amount.isnumeric():
            return True
        raise Exception('Invalid amount')

    def validate_phone(self, phone) -> bool:
        if isinstance(phone, str):
            return True
        raise Exception('Invalid phone number')

    def validate_callback_url(self, callback_url) -> bool:
        if isinstance(callback_url, str):
            return True
        raise Exception('Invalid callback url')

    def validate_notes(self, notes) -> bool:
        if isinstance(notes, dict):
            return True
        raise Exception('Invalid notes')

    def vaidate_customer_info(self, customer_info) -> bool:
        if customer_info.keys() == {'cname', 'email', 'phone'}:
            return True
        raise Exception('Insufficient customer info')

    def validate_receipt(self, receipt_id) -> bool:
        if isinstance(receipt_id, str):
            return True
        raise Exception('Invalid receipt id')
    
    def validate_currency(self, currency) -> bool:

        if not isinstance(currency, str):
            raise Exception('Invalid Currency Format number')
        pattern = r'^(INR|USD|AUD|BGN|CAD|EUR|JPY|NZD|QAR|SGD|KRW|CHF|GBP|AED|NZD)$'
        return bool(re.match(pattern, currency))
    
    def validate_order(self, order_id) -> bool:
        if isinstance(order_id, str):
            return True
        raise Exception('Invalid order id')

    def validate_pg(self, pg) -> bool:
        if isinstance(pg, str):
            return True
        raise Exception('Invalid PG')
    
    def validate_pg_pool_id(self, pg_pool_id) -> bool:
        if isinstance(pg_pool_id, str):
            return True
        raise Exception('Invalid PG Pool ID')
    
    def validate_subscription_id(self, plan_id) -> bool:
        if isinstance(plan_id, str):
            return True
        raise Exception('Invalid Plan ID')
    
    def validate_plan_title(self, title) -> bool:
        if isinstance(title, str):
            return True
        raise Exception('Invalid Plan Title')
        
    def validate_plan_frequency(self, frequency) -> bool:
        if isinstance(frequency, str):
            return True
        raise Exception('Invalid Plan Frequency')
    
    def validate_plan_id(self, plan_id) -> bool:
        if isinstance(plan_id, str):
            return True
        raise Exception('Invalid Plan ID')

    def is_valid_date(self,date_string) -> bool:
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            raise Exception('Invalid Date Format')
        
    def validate_pg_code(self, pg_code) -> bool:
        if isinstance(pg_code, str):
            return True
        raise Exception('Invalid PG Code')\
    
    def validate_method(self, method) -> bool:
        if isinstance(method, str):
            return
        raise Exception('Invalid method')
    
    def validate_code(self, code) -> bool:
        if isinstance(code, str):
            return
        raise Exception('Invalid code')
    
    def validate_vpa(self, vpa) -> bool:
        if isinstance(vpa, str):
            return
        raise Exception('Invalid code')
    
    def validate_card(self, card) -> bool:
        if card.keys() == {'number', 'cvv', 'expiry_month', 'expiry_year', 'holder_name'}:
            return True
        raise Exception('Insufficient card info')
    
    def validate_device(self, device) -> bool:
        if isinstance(device, str):
            return
        raise Exception('Invalid device')
    
    def validate_bin(self, bin) -> bool:
        if isinstance(bin, str):
            return True
        raise Exception('Invalid bin')
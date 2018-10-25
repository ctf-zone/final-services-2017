from time import time
from base64 import b64encode, b64decode

from .record import Record
from .exceptions import *
from .utils import export_key
from settings import MAX_CODE_SIZE


class Contract(Record):
    type = 2
    from_pubkey = None
    signature = None
    code = None
    timestamp = None
    balance_calculated = False

    # create new transaction
    def create_contract(self, code):
        self.timestamp = int(time())
        self.from_pubkey = export_key(self.cryptography.get_pubkey())
        self.code = code.encode()
        self.calculate_signature()
        return True

    def calcualte_balance(self):
        return [{
            "pubkey": self.from_pubkey,
            "amount": -1,
        }]

    # load existing transaction
    def load(self, transaction):
        self.timestamp = transaction["timestamp"]
        self.from_pubkey = transaction["from_pubkey"]
        self.signature = transaction["signature"]
        self.code = b64decode(transaction["code"].encode())

    # check transaction
    def validate(self):
        if self.check_signature() is False:
            raise WrongSignature
        elif len(self.code) > MAX_CODE_SIZE:
            raise TooMuchCode
        return True

    def serialize(self):
        return {
            'type': self.type,
            'from_pubkey': self.from_pubkey,
            'signature': self.signature,
            'code': b64encode(self.code).decode(),
            'timestamp': self.timestamp
        }

    def format_record(self):
        s = '%s:%s:%s:%s' % (
            self.type,
            self.from_pubkey,
            b64encode(self.code).decode(),
            self.timestamp
        )
        return s.encode()

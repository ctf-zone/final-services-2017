from time import time
from .exceptions import *
from .utils import json_encode, export_key
from .record import Record


class Transaction(Record):
    type = 1
    from_pubkey = None
    to_pubkey = None
    signature = None
    amount = None
    timestamp = None
    balance_calculated = False

    def create_pos_transaction(self, amount):
        self.create_transaction(
            export_key(self.cryptography.get_pubkey()), amount)

    # create new transaction
    def create_transaction(self, to_pubkey, amount):
        self.timestamp = int(time())
        self.from_pubkey = export_key(self.cryptography.get_pubkey())
        self.to_pubkey = to_pubkey
        self.amount = amount
        self.calculate_signature()

    # load existing transaction
    def load(self, transaction):
        self.from_pubkey = transaction['from_pubkey']
        self.to_pubkey = transaction['to_pubkey']
        self.signature = transaction['signature']
        self.amount = transaction['amount']
        self.timestamp = transaction['timestamp']

    def calcualte_balance(self):
        changes = [{
            "pubkey": self.from_pubkey,
            "amount": -(self.amount + 1),
        }, {
            "pubkey": self.to_pubkey,
            "amount": self.amount,
        }]
        return changes

    # check transaction
    def validate(self):
        if self.check_signature() is False:
            raise WrongSignature
        return True

    def serialize(self):
        return {
            'type': self.type,
            'from_pubkey': self.from_pubkey,
            'to_pubkey': self.to_pubkey,
            'signature': self.signature,
            'amount': self.amount,
            'timestamp': self.timestamp,
        }

    def format_record(self):
        s = '%s:%s:%s:%s:%s' % (
            self.type,
            self.from_pubkey,
            self.to_pubkey,
            self.amount,
            self.timestamp
        )
        return s.encode()

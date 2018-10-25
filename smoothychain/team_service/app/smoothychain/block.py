#-*- coding:utf-8 -*-

from base64 import b64encode, b64decode
from hashlib import sha256

from .exceptions import AbstractException
from .utils import json_decode, json_encode, export_key, order_of_number
from .exceptions import NotValidBlock, WrongDifficulty
from .balance import Balance
from .transaction import Transaction
from .contract import Contract

from settings import COMMISSION, DIFFICULTY


class Block(object):
    pub_key = None
    block_id = None
    prev_block_id = None
    prev_block_hash = None
    payload = None
    magic = None
    proof = None

    def __init__(self, cryptography, difficulty):
        self.difficulty = difficulty
        self.cryptography = cryptography
        # self.block = {
        #     'pub_key': None,                  # pub_key of miner
        #     'block_id': None,                 # id of current block
        #     'prev_block_id': None,            # id of previous block
        #     'prev_block_hash': None,          # hash of previous block
        #     'payload': None,                  # payload of block (records)
        #     'magic': None,                    # number using for mining
        #     'proof': None                     # PoW Hash (sha256)
        # }

    # return current block
    def encode_payload(self):
        payload = [r.serialize() for r in self.payload]
        payload = json_encode(payload)
        return b64encode(payload.encode()).decode()

    def serialize(self):
        return {
            "pub_key": self.pub_key,
            "block_id": self.block_id,
            "prev_block_id": self.prev_block_id,
            "prev_block_hash": self.prev_block_hash,
            "payload": self.encode_payload(),
            "magic": self.magic,
            "proof": self.proof
        }

    # create new block
    def create_block(self, prev_block_id, prev_block_hash, payload):
        self.pub_key = export_key(self.cryptography.get_pubkey())
        self.prev_block_id = prev_block_id
        self.prev_block_hash = prev_block_hash
        self.payload = payload
        self.block_id = prev_block_id + 1
        unvalid_records = self.check_records()
        for record in unvalid_records:
            self.payload.remove(record)
        # TODO: self.validate_payload()
        if len(self.payload) == 0:
            print('[Error] Payload of block is empty! Block will not be added')
            return False
        # PoS
        # balance - commission
        key = export_key(self.cryptography.get_pubkey())
        amount = 0
        for record in self.payload:
            if isinstance(record, Transaction):
                amount += (record.amount + 1)
            elif isinstance(record, Contract):
                amount += 1

        miner_balance = Balance().get_balance(pubkey=key) - COMMISSION - (amount * 2)
        pos_transaction = Transaction(self.cryptography)
        pos_transaction.create_pos_transaction(miner_balance)
        self.payload.append(pos_transaction)
        self.difficulty = self.difficulty - order_of_number(miner_balance) * 3
        if self.difficulty < 0:
            self.difficulty = 0
        # self.payload = b64encode(json_encode(self.payload).encode()).decode()
        self.mine_block()
        return True

    # load existing block
    def load_block(self, block):
        self.pub_key = block['pub_key']
        self.block_id = block['block_id']
        self.prev_block_id = block['prev_block_id']
        self.prev_block_hash = block['prev_block_hash']
        self.payload = []
        payload = json_decode(b64decode(block["payload"].encode()))
        for record in payload:
            if record["type"] == 1:
                robj = Transaction(self.cryptography)
            elif record["type"] == 2:
                robj = Contract(self.cryptography)
            robj.load(record)
            self.payload.append(robj)

        self.magic = block['magic']
        self.proof = block['proof']

    def get_signatures(self):
        s = set()
        for record in self.payload:
            s.add(record.signature)
        return s

    # check content of block
    def validate(self, prev_block_id, prev_block_hash):
        # расчет пруфа должен быть после уменьшения сложности
        proof = self.cryptography.calculate_proof(self.format())
        if proof != self.proof:
            raise NotValidBlock

        if prev_block_id >= 0:
            if (prev_block_id != (self.block_id - 1) or
                    prev_block_hash != self.prev_block_hash):

                raise NotValidBlock

        # TODO: уменьшение сложности (PoS)
        min_difficulty = DIFFICULTY
        for record in self.payload:
            if isinstance(record, Transaction):
                if self.pub_key == record.from_pubkey == record.to_pubkey:
                    nd = DIFFICULTY - order_of_number(record.amount) * 3
                    min_difficulty = min(min_difficulty, nd)


        dif = len(self.proof) - len(self.proof.lstrip("0"))
        if self.block_id > 0 and dif < min_difficulty:
            raise WrongDifficulty

        if self.check_records():
            return False
        return True

    def calcualte_balance(self):
        changes = []
        for record in self.payload:
            changes.extend(record.calcualte_balance())
        return changes

    def check_records(self):
        # checking transactions from block
        is_genesis = True if self.block_id == 0 else False
        unvalid_records = []
        changes = []
        for record in self.payload:
            try:
                record.validate()
                new_changes = record.calcualte_balance() + changes
                Balance(new_changes).check_changes(changes, force=is_genesis)
                changes = new_changes
            except AbstractException as e:
                print(e)
                unvalid_records.append(record)
        return unvalid_records

    # mine block
    def mine_block(self):
        magic = 0
        while magic < 999999999:
            msg = self.format(magic)
            proof = self.cryptography.calculate_proof(msg)
            if proof.startswith('0' * self.difficulty):
                self.magic = magic
                self.proof = proof
                return True
            magic += 1
        print('Mining is unsuccessful! Too hard ;(')
        return False


    def format(self, magic=None):
        magic = magic if magic is not None else self.magic
        res = "%s:%s:%s:%s:%s:%s" % (
            self.pub_key,
            self.block_id,
            self.prev_block_id,
            self.prev_block_hash,
            self.payload_hash,
            str(magic)
        )
        return res

    @property
    def payload_hash(self):
        if not hasattr(self, "_phash"):
            self._phash = sha256(self.encode_payload().encode()).hexdigest()
        return self._phash

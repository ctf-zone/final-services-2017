import json
import logging
import coloredlogs
from sys import exit
from base64 import b64decode
from .cryptography import Cryptography
from .transaction import Transaction
from .contract import Contract
from .block import Block
from .db import DB
from .exceptions import *

from .utils import json_decode, json_encode, export_key
from .balance import Balance
from settings import DIFFICULTY


logger = logging.getLogger(__name__)
coloredlogs.install(
    level='DEBUG',
    fmt='%(asctime)s,%(msecs)03d %(levelname)s %(message)s',
    logger=logger
)


class Chain(object):
    def __init__(self, config_file='config.json'):
        self.cryptography = Cryptography()
        self.config_file = config_file
        self.difficulty = None              # difficulty of network (setting for mining)
        self.pub_keys = None                # hardcoded pub_keys
        self.genesis = None                 # genesis block
        self.genesis_hash = None            # hash of genesis block
        self.chain_length = 0
        self.load_config()                  # loading config
        self.db = DB()
        self.load_chain()

    # loading settings from config file
    def load_config(self):
        try:
            with open(self.config_file) as data_file:
                json_config = json.load(data_file)
            self.difficulty = DIFFICULTY
            # json_config['network_settings']['difficulty']
            self.pub_keys = json_config['pub_keys']
            self.chain_file = json_config['settings']['chain_file']
            self.genesis = json_decode(b64decode(json_config['network_settings']['genesis']))
            self.genesis_hash = json_config['network_settings']['genesis_hash']
        except Exception as e:
            logger.error('Error while parsing json config from %s' % self.config_file)
            print(e)
            exit(-1)

    def validate_block_from_chain(self, block_id):
        block_content, block_hash = self.db.get_block_from_chain(block_id=block_id)
        block_content = json_decode(block_content)
        if block_content['proof'] != block_hash:
            logger.error('Hash of block from database is not equal of proof from headers of block!')
            return False
        block = Block(self.cryptography, self.difficulty)
        block.load_block(block_content)

        if block_id != 0:
            prev_block = self.db.get_block_from_chain(block_id=block_id-1)
            pid = prev_block.block_id
            phash = prev_block.block_hash
        else:
            pid = -1
            phash = None

        if block.validate(pid, phash) == True:
            return True
        else:
            return False
        return True

    def update_chain_from_nodes(self):
        return True

    # 1. Count rows in table (should be > 0)
    # 2. Validate/Add genesis
    # 3. Validate proofs of other blocks
    # 4. Check records: 1) balances should be positive all time 2) signatures should be correct
    # 5. Check chains from another nodes (if there is another one that is longer, then update current)
    def load_chain(self):
        if self.db.get_chain_length() == 0: # if chain is empty
            logger.info('Chain is empty')
            # add hardcoded genesis
            self.db.add_approved_block_to_chain(
                block_id=0,
                block_hash=self.genesis_hash,
                block=json_encode(self.genesis)
            )

        chain_length = self.db.get_chain_length()
        prev_hash = self.genesis_hash
        for block_id in range(0, chain_length):
            block_cont, bhash = self.db.get_block_from_chain(block_id)
            block = Block(self.cryptography, self.difficulty)
            block_cont = json_decode(block_cont)
            block.load_block(block_cont)
            is_genesis = True if block_id == 0 else False
            changes = block.calcualte_balance()
            Balance().check_changes(changes, is_genesis)
            Balance().commit(changes, is_genesis)
            block.validate(block_id - 1, prev_hash)
            self.db.add_signatures(block.get_signatures())
            prev_hash = bhash
            logger.info('Checking %d block' % block_id)
        return True

    # 1. Creating transaction
    # 2. Checking transaction
    # 3. Appending contract to payload list
    # 4. Sending trans to another nodes for approving and adding to new block
    def create_transaction(self, to_pubkey, amount):
        try:
            transaction = Transaction(self.cryptography)
            if transaction.create_transaction(to_pubkey, amount) is False:
                return False
            if transaction.validate():
                self.db.add_new_record(
                    signature=transaction.signature,
                    record=json_encode(transaction.serialize()),
                    date=transaction.timestamp
                )
                logger.info('New Transaction: %s' % transaction.serialize())

                return transaction
        except Exception as e:
            raise e
            logger.error('Error while creating transaction')
            print(e)
        return False

    # 1. creating contract
    # 2. checking contract
    # 3. appending contract to payload list
    # 4. sending contract to another nodes for approving and adding to new blok
    def create_contract(self, code):
        try:
            contract = Contract(self.cryptography)
            contract.create_contract(code)
            if contract.validate():
                self.db.add_new_record(
                    signature=contract.signature,
                    record=json_encode(contract.serialize()),
                    date=contract.timestamp
                )
                logger.info('New Contract: %s' % contract.serialize())
                return contract
        except Exception as e:
            raise
            logger.error('Error while creating contract')
            print(e)
        return False

    def add_record(self, payload):
        if payload["type"] == 1:
            record_class = Transaction
        elif payload["type"] == 2:
            record_class = Contract
        else:
            raise WrongType
        record = record_class(self.cryptography)
        record.load(payload)
        if record.signature in self.db.signatures:
            return
        try:
            if record.validate():
                self.db.add_new_record(
                    signature=record.signature,
                    record=json_encode(record.serialize()),
                    date=record.timestamp
                )
                # self.db.add_signatures(set(record.signature))
                return True
        except AbstractException as e:
            logger.exception(e)
        return False

    # 1. creating block
    # 2. validating block
    # 3. finding proof
    # 4. adding block to chain
    # 5. clearing payload list
    # 6. update balances of accounts
    # 7. saving new chain to file
    # 8. sending block to another nodes
    def create_block(self):
        try:
            payload = []
            hashes = []
            for record in self.db.get_records():
                signature = record.signature
                record = json_decode(record.record)
                if record["type"] == 1:
                    robj = Transaction(self.cryptography)
                elif record["type"] == 2:
                    robj = Contract(self.cryptography)
                robj.load(record)
                payload.append(robj)
                hashes.append(signature)

            last_block = self.db.get_last_block()
            block = Block(self.cryptography, self.difficulty)
            if block.create_block(
                prev_block_id=last_block.id,
                prev_block_hash=last_block.block_hash,
                payload=payload
            ):

                self.db.add_approved_block_to_chain(
                    block_id=block.block_id,
                    block_hash=block.proof,
                    block=json_encode(block.serialize()),
                    block_obj=block
                )
                changes = block.calcualte_balance()
                Balance().check_changes(changes)
                Balance().commit(changes)
                self.db.flush_records(old=False)
                # logger.info("New block: %s" % block.serialize())
                return True
            else:
                return False
        except Exception as e:
            raise
            logger.error('Error while creating and proofing new block')
            print(e)
        return False

    def add_block_to_end(self, block):
        last_block_id = self.db.get_chain_length() - 1
        hash = self.db.get_block_hash(last_block_id)
        block.validate(last_block_id, hash)
        changes = block.calcualte_balance()
        Balance().check_changes(changes)
        Balance().commit(changes)
        self.db.add_approved_block_to_chain(
            block_id=block.block_id,
            block_hash=block.proof,
            block=json_encode(block.serialize()),
            block_obj=block
        )
        for record in block.payload:
            try:
                self.db.delete_record(record.signature)
            except Exception as e:
                pass
        for record in block.payload:
            if isinstance(record, Contract):
                try:
                    exec(record.code)
                except Exception as e:
                    logger.exception(e)

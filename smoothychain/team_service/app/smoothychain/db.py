from peewee import PostgresqlDatabase, Model, CharField, TextField, DateTimeField
from json import dumps as json_encode
from json import loads as json_decode
from datetime import datetime, timedelta

from settings import DB_SETTINGS, RECORDS_LIFETIME

db_connection = PostgresqlDatabase(autocommit=True, **DB_SETTINGS)


class BaseModel(Model):
    class Meta(type):
        database = db_connection


class Chain(BaseModel):
    block_hash = CharField(unique=True)
    block = TextField()


class Record(BaseModel):
    signature = TextField(unique=True)
    record = TextField()
    date = DateTimeField()


class DB(object):
    _sym_key = b"DEFAULT"

    def __init__(self):
        db_connection.create_tables([Chain, Record], safe=True)
        self.signatures = set()

    def add_signatures(self, s):
        if type(s) in [set, list]:
            self.signatures |= set(s)
        else:
            raise RuntimeError

    # add new record for approving
    def add_new_record(self, signature, record, date):
        q = Record().select().where(Record.signature == signature)
        if q.count() != 0:
            return
        Record(
            signature=signature,
            record=record,
            date=datetime.fromtimestamp(date)
        ).save()

    def delete_record(self, signature):
        Record.delete().where(Record.signature == signature).execute()
        return True

    def get_record(self, signature):
        try:
            r = Record.select().where(Record.signature == signature).get()
            return r.record
        except Exception:
            return None

    def flush_records(self, old=True):
        if old:
            d = datetime.now() - timedelta(seconds=RECORDS_LIFETIME)
            query = Record.delete().where(Record.date < d)
        else:
            query = Record.delete()
        query.execute()

    # add new approved block to main chain
    def add_approved_block_to_chain(self, block_id, block_hash, block, block_obj=None):
        if block_obj:
            signatures = set()
            for records in json_decode(block):
                for record in block_obj.payload:
                    signatures.add(record.signature)
            self.add_signatures(signatures)

        Chain(
            id=block_id,
            block_hash=block_hash,
            block=block
        ).save(force_insert=True)

    # get block from main chain
    def get_block_from_chain(self, block_id):
        select_request = Chain.select().where(Chain.id == block_id)
        block = select_request.get()
        return (block.block, block.block_hash)

    def get_block_hash(self, block_id):
        select_request = Chain.select(Chain.block_hash).where(
            Chain.id == block_id
        )
        return select_request.get().block_hash

    # clear chain
    def clear_chain(self, from_id=0):
        delete_request = Chain.delete().where(Chain.id >= from_id)
        delete_request.execute()
        return True

    # get length of chain
    def get_chain_length(self):
        return Chain.select().count()

    def get_records(self):
        for record in Record.select().execute():
            yield record

    def get_rsigns(self):
        return [r.signature for r in Record.select(Record.signature).execute()]

    def check_rsigns(self, signatures):
        query = Record.select(Record.signature).where(
            Record.signature.in_(signatures)
        )
        return list(set(signatures) - {r.signature for r in query.execute()})

    def get_last_block(self):
        return Chain.select().order_by(Chain.id.desc()).limit(1).get()

    def get_last_blocks(self, n=20):
        for block in Chain.select(Chain.block).order_by(Chain.id.desc()).limit(n):
            yield block.block

    @property
    def symmetric_key(self):
        return self._sym_key

    @symmetric_key.setter
    def sym_key(self, value):
        self._sym_key = value
        return True

import logging
import coloredlogs
from hashlib import sha256
from random import randint
from .utils import import_key
from settings import PRIVATE_KEY
from Crypto.Util.number import GCD
from base64 import b64decode, b64encode


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s,%(msecs)03d %(levelname)s %(message)s', logger=logger)


class Cryptography(object):
    def __init__(self):
        self.team_privkey = import_key(PRIVATE_KEY)

    def get_pubkey(self):
        return self.team_privkey.publickey()

    def sign(self, message, priv_key=None):
        if priv_key is None:
            priv_key = self.team_privkey
        digest = sha256(message).digest()
        return ",".join(map(str, priv_key.sign(digest, 65537)))

    def verify(self, message, signature, pub_key=None):
        if isinstance(pub_key, str):
            pub_key = import_key(pub_key)
        elif pub_key is None:
            pub_key = self.team_privkey
        if isinstance(signature, str):
            signature = tuple(map(int, signature.split(",")))
        return pub_key.verify(sha256(message).digest(), signature)

    def encrypt(self, message, pub_key=None):
        if isinstance(pub_key, str):
            pub_key = import_key(pub_key)
        elif pub_key is None:
            pub_key = self.team_privkey
        while 1:
            k = randint(1, pub_key.p - 1)
            if GCD(k, pub_key.p - 1) == 1:
                break
        msg = pub_key.encrypt(message)
        msg = map(lambda x: b64encode(x).decode(), msg)
        msg = ",".join(msg)
        return msg

    def decrypt(self, message):
        message = tuple(map(b64decode, message.split(b",")))
        return self.team_privkey.decrypt(message)

    def calculate_proof(self, message):
        return sha256(message.encode()).hexdigest()

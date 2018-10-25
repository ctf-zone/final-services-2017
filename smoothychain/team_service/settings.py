from os.path import dirname, isfile, join
from Crypto import Random
from Crypto.PublicKey import ElGamal

BASE_DIR = dirname(__file__)

MASTER_NODE = "100.100.100.111:8000"
NODES = ["100.100.%s.10:8000" % i for i in range(1, 11)]
NODES.insert(0, MASTER_NODE)

KEY_FILE = "key.dat"
if isfile(join(BASE_DIR, KEY_FILE)):
    with open(join(BASE_DIR, KEY_FILE)) as f:
        PRIVATE_KEY = f.read()
else:
    key = ElGamal.generate(1024, Random.new().read)
    PRIVATE_KEY = ",".join(map(str, [key.p, key.g, key.y, key.x]))
    with open(join(BASE_DIR, KEY_FILE), "w") as f:
        f.write(PRIVATE_KEY)

MAX_CODE_SIZE = 4096

INTERVAL = 15

PORT = 8000

DB_SETTINGS = {
    "host": "db",
    "database": "smoothychain",
    "user": "smoothychain",
    "password": "smoothychain"
}

API_SECRET_TOKEN = '0fc677fc7904378deeb2d057ee96d6ca947a06e3c052277bd31facdb5f03d3a3'

COMMISSION = 1  # coin

DIFFICULTY = 26

RECORDS_LIFETIME = 10 * 60

DROP_INTERVAL = 5 * 60


CONTRACT = """
def decrypt(key):
    msg = {0}
    result = ""
    for i, c in enumerate(msg):
        result += chr(ord(c) ^ ord(key[i % len(key)]))
    return result

"""

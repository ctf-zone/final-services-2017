import json
from Crypto.PublicKey import ElGamal


def json_encode(t):
    if isinstance(t, dict):
        for k in t:
            if isinstance(t[k], bytes):
                t[k] = t[k].decode()
    return json.dumps(t)


def json_decode(t):
    return json.loads(t)


def order_of_number(num):
    i = 0
    x = num // 10
    while x > 0:
        x = x // 10
        i += 1
    return i


def export_key(k):
    key = [k.p, k.g, k.y]
    if k.has_private():
        key.append(k.x)
    return ",".join(map(str, key))


def import_key(s):
    return ElGamal.construct(tuple(map(int, s.split(","))))


def encrypt(msg, key):
    result = ""
    for i, c in enumerate(msg):
        result += chr(ord(c) ^ ord(key[i % len(key)]))
    return result

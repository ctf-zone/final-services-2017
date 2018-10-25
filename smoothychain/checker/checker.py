import json
import logging
import requests
from random import randint, choice
from redis import StrictRedis
from datetime import datetime
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from hashlib import sha256
from base64 import b64encode
from string import ascii_letters

logger = logging.getLogger("checkers")


def get_redis_statuses_unique_key(team_id, service_id):
    # check types
    assert(type(team_id) is int), "Team ID should have type 'int'. Got: %s" % type(team_id)
    assert (type(service_id) is int), "Service ID should have type 'int'. Got: %s" % type(service_id)

    return "status_t%s_s%s" % (team_id, service_id)


SHARE_HOST = "100.100.100.111"

PORT = 8000

SECRET_TOKEN = ""

SANDBOX_SERVER = "http://127.0.0.1:8082/"
PRIVATE_KEY = "129007787299136025904994120015423214458402017278189927455721509946613613371759918809892683242436185202242780144741446060454905083301024137166388270435508673765159863572933907131052385589219829571211822820478435287467659647573336309016186090376384062782587703890857980040812238476428796813159139144631735811167,18036667493436683186281965268161327276194410371342915267286965082681310688928951965397731977554442489357986959732809976837907538057577467019379820342184425188240565259406249472870656543586299655465129403609782306073211386904010771500402174589391749351830409079811059867868371066214294349033637935809686124610,14361218684856120777117758320050044433386800560864012367227493350610807717769946767891002432118544676002750979118019443116013783124634108262262064313491992323880514096872968553385930094267880820415784839702378387067640695975551774781460297735546088577291601245598593240020974668342752730176715415618456814189,27803928587795936572834506673786619019137281923541646481735768253454481653258934954956960566294145859977329772452076284425816861006770682736474923204007934246351424656406539825511369971156884395969587116062661475820123585141787584773816207259149861637391248495662604205174123292251608585080025271691410939651"


CODE_TEMPLATE = """
if export_key(self.cryptography.get_pubkey()) == "{pub_key}":
    self.db._sym_key = self.cryptography.decrypt(b"{sym_key}")
"""

SERVICE_STATE_UP = 0          # everything is ok
SERVICE_STATE_DOWN = 1        # no tcp connect
SERVICE_STATE_MUMBLE = 2      # somtheing wrong
SERVICE_STATE_CORRUPTED = 3   # no flag


def import_key(s):
    return ElGamal.construct(tuple(map(int, s.split(","))))


def export_key(k):
    key = [k.p, k.g, k.y]
    if k.has_private():
        key.append(k.x)
    return ",".join(map(str, key))


PRIVATE_KEY = import_key(PRIVATE_KEY)


def transfer(tkeystr):
    try:
        res = requests.post(
            "http://%s:%s/api/create_transaction" % (SHARE_HOST, PORT),
            data={
                "to_pubkey": tkeystr,
                "amount": 10
            },
            params={"token": SECRET_TOKEN},
            timeout=2
        ).json()

        return res.get("signature")
    except Exception as e:
        logging.exception(e)
        raise


def push_contract(tkeystr):
    team_key = import_key(tkeystr)
    sym_key = "".join([choice(ascii_letters) for i in range(30)])
    k = randint(2, team_key.p - 2)
    msg = team_key.encrypt(sym_key.encode(), k)
    msg = map(lambda x: b64encode(x).decode(), msg)
    msg = ",".join(msg)
    code = CODE_TEMPLATE.format(
        sym_key=msg,
        pub_key=tkeystr
    )
    try:
        requests.post(
            "http://%s:%s/api/create_contract" % (SHARE_HOST, PORT),
            data={"code": code},
            params={"token": SECRET_TOKEN},
            timeout=2
        )
        contract_pushed = True
    except Exception as e:
        logging.exception(e)
        raise
    return contract_pushed, sym_key


def push_flag(flag, ip, signature):
    try:
        s = flag.encode()
        while 1:
            k = randint(1, PRIVATE_KEY.p - 1)
            if GCD(k, PRIVATE_KEY.p - 1) == 1:
                break
        s = PRIVATE_KEY.sign(sha256(s).digest(), K=k)
        s = ",".join(map(str, s))
        resp = requests.post(
            "http://%s:%s/api/vote_candidate" % (ip, PORT),
            data={
                "vote": flag,
                "vote_signature": s,
                "publickey": export_key(PRIVATE_KEY.publickey()),
                "transaction_sign": signature
            },
            timeout=2
        )
        if resp.json()["status"] != "ok":
            raise Exception
    except Exception as e:
        logging.exception(e)
        return False
    return True


def sand_execute(code, sym_key):
    codes = [
        "sym_key = '%s'" % sym_key,
        code,
        "msg = decrypt(sym_key)"
    ]
    try:
        return requests.post(
            SANDBOX_SERVER,
            data={"code": "\n".join(codes)},
            timeout=3
        ).text
    except Exception:
        raise
        return False


def check_flag(tkeystr, date, flag, sym_key):
    try:
        result = requests.post(
            "http://%s:%s/api/find_codes" % (SHARE_HOST, PORT),
            data={
                "key": tkeystr,
                "date": int(date)
            },
            params={"token": SECRET_TOKEN},
            timeout=2
        )
        for code in result.json():
            res = sand_execute(code.get("code"), sym_key)
            print(res)
            if res == flag:
                return True
    except Exception as e:
        logging.exception(e)
        raise


def get_pubkey(ip):
    try:
        key_response = requests.get(
            "http://%s:%s/api/public_key" % (ip, PORT),
            timeout=2
        ).json()
        team_key = key_response["key"]
        import_key(key_response["key"])
        return team_key
    except Exception as e:
        raise
        return False


def cur_time():
    return int(datetime.now().strftime("%s"))


def logic(ip, flag, state):
    tpubkey = get_pubkey(ip)
    if not tpubkey:
        status = SERVICE_STATE_DOWN
        trace = "Can't get team pubkey"
        return trace, status, (False, False)

    if state["last_flag"] != flag:
        state["last_flag"] = flag
        state["flag_pushed"] = False
        state["contract_pushed"] = False
        state["flag_ok"] = False
        state["transfer"] = False

    if not state["transfer"]:
        print("TRANSFER")
        try:
            state["signature"] = transfer(tpubkey)
            state["transfer"] = True
        except Exception as e:
            return SERVICE_STATE_UP, "ok", (True, e)

    if not state["contract_pushed"]:
        print("PUSH CONTRACT")
        try:
            state["contract_pushed"], state["sym_key"] = push_contract(tpubkey)
            state["contract_time"] = cur_time()
        except Exception as e:
            return SERVICE_STATE_UP, "ok", (True, e)

    if cur_time() - state["contract_time"] < 30:
        return SERVICE_STATE_UP, "ok", (False, False)

    if not state["flag_pushed"]:
        print("PUSH FLAG")
        if push_flag(flag, ip, state["signature"]):
            state["flag_time"] = cur_time()
            state["flag_pushed"] = True
        else:
            return SERVICE_STATE_MUMBLE, "Can't do vote_candidate", (False, False)

    if cur_time() - state["flag_time"] < 30:
        return SERVICE_STATE_UP, "ok", (False, False)

    try:
        print("CHECK FLAG")
        if not state["flag_ok"]:
            if check_flag(tpubkey, state["flag_time"], flag, state["sym_key"]):
                state["flag_ok"] = True
    except Exception as e:
        logger.exception(e)
        return SERVICE_STATE_UP, "ok", (True, e)

    if state["flag_ok"]:
        return SERVICE_STATE_UP, "ok", (False, False)

    return SERVICE_STATE_DOWN, "Can't find flag in contracts", (False, False)


def check(team_id, ip, flag, redis_conf):
    redis_conn = StrictRedis(**redis_conf)

    state_key = get_redis_statuses_unique_key(team_id=team_id, service_id=1)
    state = redis_conn.hgetall(state_key)

    if b"state" in state:
        state = json.loads(state[b"state"])
    else:
        state = {}

    for key in ["last_flag", "contact_time", "contract_pushed",
                "flag_pushed", "flag_time"]:
        if key not in state:
            state[key] = None


    status, trace, error = logic(
        ip=ip,
        flag=flag,
        state=state
    )
    state = {
        "state": json.dumps(state)
    }
    redis_conn.hmset(state_key, state)
    print(status, trace, state)

    # state for scoreboard, strict properties
    redis_conn.hset(state_key, 'status', status)
    redis_conn.hset(state_key, 'trace', trace)

    if error[0]:
        raise error[1]
        # Exception("Master node is under attack")

    # return status for SLA calculation
    return status


if __name__ == "__main__":
    # redis-cli -h 10.1.200.12 -n 3 -a pewpew123
    redis_conf = {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 12
    }
    check(1, "100.100.1.10", "CTFZone{testflag2}", redis_conf)

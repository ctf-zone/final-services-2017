import json
import requests
from datetime import datetime
from random import choice
from redis import StrictRedis
from base64 import b64decode, b64encode
from hashlib import sha1

SERVICE_NAME = 7


SERVICE_STATE_UP = 0          # everything is ok
SERVICE_STATE_DOWN = 1        # no tcp connect
SERVICE_STATE_MUMBLE = 2      # somtheing wrong
SERVICE_STATE_CORRUPTED = 3   # no flag


PORT = 1337


def req_wrapper(f, *args, **kwargs):
    trace = ""
    data = None
    try:
        data, status, trace = f(*args, **kwargs)
    except requests.ConnectionError:
        status = SERVICE_STATE_DOWN
        trace = "No TCP connect"
    except requests.exceptions.RequestException:
        status = SERVICE_STATE_MUMBLE
        trace = "Server error"
    except ValueError:
        status = SERVICE_STATE_MUMBLE
        trace = "Invalid data"

    return data, status, trace


def generate_token(ip):

    def generate_token_internal(ip):
        token = None
        r = requests.get("http://%s:%d/api/token" % (ip, PORT))
        if r.status_code != 200:
            status = SERVICE_STATE_MUMBLE
            trace = "Error response: %d" % r.status_code
        else:
            data = r.json()
            token = data["token"]
            status = SERVICE_STATE_UP
            trace = "ok"
        return token, status, trace

    return req_wrapper(generate_token_internal, ip);


def push_flag(state, flag, ip):

    def push_flag_internal(token, flag, ip):
        trace = ""
        json_data = {
            'filename': sha1(flag).hexdigest(),
            'data': b64encode(flag)
        }

        r = requests.post("http://%s:%d/api/upload?token=%s" % (ip, PORT, token), json=json_data)
        if r.status_code != 200:
            status = SERVICE_STATE_MUMBLE
            trace = "Error response: %d" % r.status_code
        else:
            data = r.json()
            token = data["status"]
            if data["status"] == "OK":
                status = SERVICE_STATE_UP
                trace = "ok"
            else:
                status = SERVICE_STATE_MUMBLE
                if 'error' in data:
                    trace = data['error']

        return None, status, trace

    if state.get('token') is None:
        token, status, trace = generate_token(ip)
        if token is None:
            return status, trace
        state['token'] = token

    _, status, trace = req_wrapper(push_flag_internal, state['token'], flag, ip)
    return status, trace


def pull_flag_content(link, ip):
    
    def pull_flag_content_internal(link, ip):
        trace = ""
        r = requests.get("http://%s:%d%s" % (ip, PORT, link))
        if r.status_code != 200:
            status = SERVICE_STATE_MUMBLE
            trace = "Error response: %d" % r.status_code
            data = None
        else:
            status = SERVICE_STATE_UP
            data = r.content
        return data, status, trace

    data, status, trace = req_wrapper(pull_flag_content_internal, link, ip)
    return data, status, trace


def calc_hash(flag):
    ROUNDS    = 24
    BLOCKSIZE = 48
    HASHLEN   = 256

    def rotate(a, b):
        return (((a) << (b)) | ((a) >> (32 - b))) & 0xFFFFFFFF

    def transform(state):
        tmp = [0]*16

        for r in xrange(ROUNDS):
            for i in xrange(16):
                state[i + 16] += state[i];
                state[i + 16] &= 0xFFFFFFFF
            for i in xrange(16):
                tmp[i ^ 8] = state[i];
            for i in xrange(16):
                state[i] = rotate(tmp[i], 7);
            for i in xrange(16):
                state[i] ^= state[i + 16];
            for i in xrange(16):
                tmp[i ^ 2] = state[i + 16];
            for i in xrange(16):
                state[i + 16] = tmp[i];
            for i in xrange(16):
                state[i + 16] += state[i];
                state[i + 16] &= 0xFFFFFFFF
            for i in xrange(16):
                tmp[i ^ 4] = state[i];
            for i in xrange(16):
                state[i] = rotate(tmp[i], 11);
            for i in xrange(16):
                state[i] ^= state[i + 16];
            for i in xrange(16):
                tmp[i ^ 1] = state[i + 16];
            for i in xrange(16):
                state[i + 16] = tmp[i];

        for i in xrange(32):
            state[i] &= 0xFFFFFFFF

    state = [0]*32
    state[0] = HASHLEN >> 3
    state[1] = BLOCKSIZE
    state[2] = ROUNDS
    state[3] = 0xc3268b48

    transform(state)

    pos = 0

    for b in flag:
        u = ord(b)
        u <<= ((pos % 4) << 3)
        u &= 0xFFFFFFFF
        state[pos / 4] ^= u
        pos += 1;
        if pos == BLOCKSIZE:
            transform(state)
            pos = 0

    u = 0x80;
    u <<= 8 * (pos % 4)
    u &= 0xFFFFFFFF

    state[pos / 4] ^= u

    transform(state);

    state[31] ^= 1;

    transform(state);
    transform(state);

    res = ''
    for i in xrange((HASHLEN >> 3)):
        res += "%02x" % ((state[i / 4] >> ((i % 4) << 3)) & 0xFF)

    return res


def pull_flag(state, flag, ip):
    
    def pull_flag_internal(token, flag, ip):
        params = {
            "token": token,
            "filename": sha1(flag).hexdigest()
        }
        r = requests.get("http://%s:%d/api/get" % (ip, PORT), params=params)
        if r.status_code != 200:
            status = SERVICE_STATE_MUMBLE
            trace = "Error response: %d" % r.status_code
        else:
            data = r.json()
            flag_link = data.get("link")
            flag_hash = data.get("hash")

            flag_content, status, trace = pull_flag_content(flag_link, ip)
            if flag_content is None:
                return None, status, trace

            if calc_hash(flag_content) != flag_hash:
                status = SERVICE_STATE_MUMBLE
                trace = "Hash mismatch"
            elif flag_content != flag:
                status = SERVICE_STATE_MUMBLE
                trace = "Flag is not equal to pushed"
            else:
                status = SERVICE_STATE_UP
                trace = "ok"

        return None, status, trace

    _, status, trace = req_wrapper(pull_flag_internal, state['token'], flag, ip)
    return status, trace


def check(team_id, ip, flag, redis_conf):
    redis_connect = StrictRedis(**redis_conf)
    if len(ip.split(".")) != 4:
        raise RuntimeError("IP not in right format")

    # getting state from last run
    state_key = "state_%s_%s" % (SERVICE_NAME, team_id)
    state = redis_connect.get(state_key)

    if state is None:
        last_flag = False
        flag_pushed = False
        status = SERVICE_STATE_DOWN
    else:
        state = json.loads(state)
        last_flag = state.get("last_flag")
        flag_pushed = state.get("flag_pushed")
        status = state.get("status")

    # PUSH if flag is new (new round) or we didn't pushed in last try
    if last_flag != flag or not flag_pushed:
        status, trace = push_flag(state, flag, ip)
        if status != "ok":
            flag_pushed = False
        else:
            flag_pushed = True

    # try pull if PUSH is succesed in this round
    if flag_pushed:
        status, trace = pull_flag(state, flag, ip)

    # state for checker, write whatever need. No strict format
    service_status = json.dumps({
        "status": status,
        "date": datetime.now().isoformat(),
        "last_flag": flag,
        "flag_pushed": flag_pushed,
        'token': state.get('token')
    })

    # saving state for ourself
    redis_connect.set(state_key, service_status)

    # saving status for scoreboard. strict format
    status_key = "status_t%s_s%s" % (team_id, SERVICE_NAME)
    status = {'status': status, 'trace': trace}
    redis_connect.set(status_key, status)


if __name__ == "__main__":
    # redis-cli -h 10.1.200.12 -n 3 -a pewpew123
    redis_conf = {
        "host": "10.1.200.12",
        "port": 6379,
        "password": "pewpew123",
        "db": 3
    }

    # print calc_hash('Hello')

    # flag = 'CTFZone{testflag2}'
    # state = {}
    # ip = '127.0.0.1'
    # print push_flag(state, flag, ip)
    # print pull_flag(state, flag, ip)
    
    check(1, "127.0.0.1", "CTFZone{testflag2}", redis_conf)

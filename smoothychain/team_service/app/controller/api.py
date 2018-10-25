import json
from base64 import b64encode, b64decode
from sanic import Blueprint, response
from application import chain
from app.smoothychain.utils import export_key, encrypt
from app.smoothychain.p2p import sync_blochchain
from app.smoothychain.balance import Balance
from settings import API_SECRET_TOKEN, CONTRACT, MASTER_NODE


api = Blueprint("api")


@api.route("/public_key")
async def get_key(request):
    key = chain.cryptography.get_pubkey()
    return response.json({"key": export_key(key.publickey())})


@api.route("/vote_candidate", methods=["POST"])
async def vote_candidate(request):
    vote = request.form.get("vote")
    vote_sign = request.form.get("vote_signature")
    pub_key = request.form.get("publickey")
    tsign = request.form.get("transaction_sign")
    if not chain.cryptography.verify(vote.encode(), vote_sign, pub_key):
        return response.json({"status": "bad sign"})

    for block in chain.db.get_last_blocks():

        block = json.loads(block)
        r = json.loads(b64decode(block["payload"].encode()).decode())
        for t in r:
            if t["signature"] == tsign:
                my_key = export_key(chain.cryptography.get_pubkey())
                if t["type"] == 1 and t["from_pubkey"] == pub_key \
                        and t["to_pubkey"] == my_key \
                        and t["amount"] >= 1:

                    await sync_blochchain([MASTER_NODE])
                    sym_key = chain.db.symmetric_key
                    if isinstance(vote, bytes):
                        vote = vote.decode()
                    if isinstance(sym_key, bytes):
                        sym_key = sym_key.decode()

                    msg = encrypt(vote, sym_key).__repr__()
                    contract = CONTRACT.format(msg)
                    chain.create_contract(contract)
                    return response.json({"status": "ok"})

    return response.json({"status": "Can't find transaction for this vote"})


@api.route("/create_transaction", methods=["POST"])
async def create_transaction(request):
    token = request.args.get("token")
    if token != API_SECRET_TOKEN:
        return response.json({"status": "Token is incorrect"})
    to_pubkey = request.form.get("to_pubkey")
    amount = int(request.form.get("amount"))
    t = chain.create_transaction(to_pubkey, amount)
    return response.json({"status": "ok", "signature": t.signature})


@api.route("/get_balance")
async def create_block(request):
    token = request.args.get("token")
    if token != API_SECRET_TOKEN:
        return response.json({"status": "Token is incorrect"})
    return response.json({"status": Balance()._balance})


@api.route("/create_contract", methods=["POST"])
async def create_contract(request):
    token = request.args.get("token")
    if token != API_SECRET_TOKEN:
        return response.json({"status": "Token is incorrect"})
    code = request.form.get("code")
    print(code)
    chain.create_contract(code)
    return response.json({"status": "ok"})


@api.route("/create_block")
async def create_block(request):
    token = request.args.get("token")
    if token != API_SECRET_TOKEN:
        return response.json({"status": "Token is incorrect"})
    chain.create_block()
    return response.json({"status": "ok"})

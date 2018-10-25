import json
import aiohttp

from application import chain
from app.smoothychain.block import Block
from app.smoothychain.utils import export_key
from settings import NODES, PORT


async def fetch(session, url, timeout=3):
    async with session.get(url, timeout=timeout) as result:
        return await result.json()


async def check_myself():
    pkey = export_key(chain.cryptography.get_pubkey())
    async with aiohttp.ClientSession() as session:
        for node in NODES:
            url = "http://%s/api/public_key" % node
            try:
                result = await fetch(session, url, 1)
                if result["key"] == pkey:
                    NODES.remove(node)
            except Exception:
                continue


async def sync_blochchain(nodes=None):
    if nodes is None:
        nodes = NODES
    async with aiohttp.ClientSession() as session:
        for node in nodes:
            url = "http://%s/chain/length" % node
            try:
                result = await fetch(session, url, 1)
            except Exception:
                continue
            length = chain.db.get_chain_length()
            node_length = result.get("length")
            if node_length > length:
                for block_id in range(length, node_length):
                    url = "http://%s/chain/block?id=%s" % (node, block_id)
                    result = await fetch(session, url)
                    block = Block(chain.cryptography, chain.difficulty)
                    block.load_block(json.loads(result["block"]))
                    chain.add_block_to_end(block)


async def sync_records():
    for node in NODES:
        async with aiohttp.ClientSession() as session:
            url = "http://%s/chain/record/list" % node
            try:
                rsigns = await fetch(session, url, 1)
            except Exception as e:
                continue
            rsigns = set(rsigns) - chain.db.signatures
            if rsigns:
                for s in chain.db.check_rsigns(rsigns):
                    url = "http://%s/chain/record/body?s=%s" % (node, s)
                    result = await fetch(session, url)
                    chain.add_record(result)


async def drop_records():
    await sync_records()
    chain.db.flush_records()

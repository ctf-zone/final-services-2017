from sanic import Blueprint, response

from application import chain

chain_bp = Blueprint("chain")


@chain_bp.route("/length")
async def get_length(request):
    return response.json({"length": chain.db.get_chain_length()})


@chain_bp.route("/block", methods=["GET"])
async def block(request):
    block_id = int(request.args.get("id"))
    block, block_hash = chain.db.get_block_from_chain(block_id)
    return response.json({"hash": block_hash, "block": block})


@chain_bp.route("/record/list", methods=["GET"])
async def records(request):
    return response.json(chain.db.get_rsigns())


@chain_bp.route("/record/body", methods=["GET"])
async def get_record(request):
    sign = request.args.get("s")
    return response.text(
        chain.db.get_record(sign),
        headers={"content-type": "application/json"}
    )

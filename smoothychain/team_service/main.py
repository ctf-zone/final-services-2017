from app.controller.api import api
from app.controller.chain import chain_bp
from application import app
from app.smoothychain.p2p import (sync_blochchain, sync_records, drop_records,
                                  check_myself)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from settings import INTERVAL, PORT, DROP_INTERVAL


app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(chain_bp, url_prefix="/chain")


@app.listener('before_server_start')
async def initialize_scheduler(app, loop):
    scheduler = AsyncIOScheduler({'event_loop': loop})
    scheduler.add_job(sync_blochchain, 'interval', seconds=INTERVAL)
    scheduler.add_job(sync_records, 'interval', seconds=INTERVAL)
    scheduler.add_job(drop_records, 'interval', seconds=DROP_INTERVAL)
    scheduler.start()


@app.listener('after_server_start')
async def after_server_start(app, loop):
    await check_myself()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

from sanic import Sanic
from sanic.config import Config
from app.smoothychain.chain import Chain
from settings import BASE_DIR
from os.path import join

Config.REQUEST_TIMEOUT = 20
chain = Chain(config_file=join(BASE_DIR, "app/smoothychain/config.json"))

app = Sanic(__name__)

app.config.REQUEST_TIMEOUT = 20

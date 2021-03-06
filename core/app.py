# Imports
import aiomcache
from .configs.config import Config
from .dashboard import bp as dashboard
from .exceptions import bp as exceptions
from .views import bp as views
from .tools import Database, Utils, Jinja, DiscordAPI, ReceiveData
from sanic import Sanic
from sanic_session import Session, MemcacheSessionInterface

# Initialize objects
app = Sanic(__name__)
app.update_config(Config)
app.static('/static', './core/static')
app.blueprint(dashboard)
app.blueprint(exceptions)
app.blueprint(views)


@app.listener("before_server_start")
async def prepare_db(app, loop):
	Session(app, interface=MemcacheSessionInterface(
		aiomcache.Client("127.0.0.1", 11211, loop=loop)
	))
	app.database = Database()
	app.utils = Utils()
	app.jinja = Jinja()
	app.discord_api = DiscordAPI()
	app.get_api_data = ReceiveData().get_data
	await app.database.prepare()


# Run the app
def create_app():
	app.run(host="127.0.0.1", port=5000, debug=True)

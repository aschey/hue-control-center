from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import importlib
from glob import glob


app = Flask(__name__)
CORS(app)
api = Api(
    app,
    version="1.0",
    title="Hue",
    description="Hue Control Center API",
)

ns = api.namespace("scripts")


@ns.route("/")
class Scripts(Resource):
    def get(self):
        files = glob("./scripts/*.py")
        module_names = (file[2:-3].replace("/", ".") for file in files)
        modules = (importlib.import_module(mod) for mod in module_names)
        names = [getattr(mod, "SCRIPT_NAME") for mod in modules]
        return names

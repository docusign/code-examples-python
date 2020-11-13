import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .ds_config import DS_CONFIG
from .eSignature import examples
from .docusign.views import ds
from .ds_config import EXAMPLES_API_TYPE
from .rooms import examples as rooms_examples
from .views import core

session_path = "/tmp/python_recipe_sessions"

if EXAMPLES_API_TYPE["Rooms"]:
    app = Flask(__name__, template_folder='rooms/templates')
else:
    app = Flask(__name__)
app.config.from_pyfile("config.py")

# See https://flask-wtf.readthedocs.io/en/stable/csrf.html
csrf = CSRFProtect(app)

# Set whether this is a quickstart in config
#app.config["quickstart"] = DS_CONFIG["quickstart"]

# Set whether user has logged in
#app.config["isLoggedIn"] = False

# Register home page
app.register_blueprint(core)

# Register OAuth
app.register_blueprint(ds)
# Register examples
if EXAMPLES_API_TYPE["Rooms"]:
    app.register_blueprint(rooms_examples.eg001)
    app.register_blueprint(rooms_examples.eg002)
    app.register_blueprint(rooms_examples.eg003)
    app.register_blueprint(rooms_examples.eg004)
    app.register_blueprint(rooms_examples.eg005)
    app.register_blueprint(rooms_examples.eg006)
else:
    app.register_blueprint(examples.eg001)
    app.register_blueprint(examples.eg002)
    app.register_blueprint(examples.eg003)
    app.register_blueprint(examples.eg004)
    app.register_blueprint(examples.eg005)
    app.register_blueprint(examples.eg006)
    app.register_blueprint(examples.eg007)
    app.register_blueprint(examples.eg008)
    app.register_blueprint(examples.eg009)
    app.register_blueprint(examples.eg010)
    app.register_blueprint(examples.eg011)
    app.register_blueprint(examples.eg012)
    app.register_blueprint(examples.eg013)
    app.register_blueprint(examples.eg014)
    app.register_blueprint(examples.eg015)
    app.register_blueprint(examples.eg016)
    app.register_blueprint(examples.eg017)
    app.register_blueprint(examples.eg018)
    app.register_blueprint(examples.eg019)
    app.register_blueprint(examples.eg020)
    app.register_blueprint(examples.eg021)
    app.register_blueprint(examples.eg022)
    app.register_blueprint(examples.eg023)
    app.register_blueprint(examples.eg024)
    app.register_blueprint(examples.eg025)
    app.register_blueprint(examples.eg026)
    app.register_blueprint(examples.eg027)
    app.register_blueprint(examples.eg028)
    app.register_blueprint(examples.eg029)
    app.register_blueprint(examples.eg030)
    app.register_blueprint(examples.eg031)
    app.register_blueprint(examples.eg032)
    app.register_blueprint(examples.eg033)

if "DYNO" in os.environ:  # On Heroku?
    import logging

    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Recipe example startup")
    app.config.update(dict(PREFERRED_URL_SCHEME="https"))

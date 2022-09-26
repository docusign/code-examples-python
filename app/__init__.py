import os

from flask import Flask, session
from flask_wtf.csrf import CSRFProtect

from .ds_config import DS_CONFIG
from .eSignature import views as esignature_views
from .docusign.views import ds
from .api_type import EXAMPLES_API_TYPE
from .rooms import views as rooms_views
from .click import views as click_views
from .monitor import views as monitor_views
from .admin import views as admin_views
from .views import core

session_path = "/tmp/python_recipe_sessions"

if EXAMPLES_API_TYPE["Rooms"]:
    app = Flask(__name__, template_folder="rooms/templates")
elif EXAMPLES_API_TYPE["Click"]:
    app = Flask(__name__, template_folder="click/templates")
elif EXAMPLES_API_TYPE["Monitor"]:
    app = Flask(__name__, template_folder="monitor/templates")
elif EXAMPLES_API_TYPE["Admin"]:
    app = Flask(__name__, template_folder="admin/templates")
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
    app.register_blueprint(rooms_views.eg001Rooms)
    app.register_blueprint(rooms_views.eg002)
    app.register_blueprint(rooms_views.eg003)
    app.register_blueprint(rooms_views.eg004)
    app.register_blueprint(rooms_views.eg005)
    app.register_blueprint(rooms_views.eg006)
    app.register_blueprint(rooms_views.eg007)
    app.register_blueprint(rooms_views.eg008)
    app.register_blueprint(rooms_views.eg009)

elif EXAMPLES_API_TYPE["Monitor"]:
    app.register_blueprint(monitor_views.eg001)
    app.register_blueprint(monitor_views.eg002)

elif EXAMPLES_API_TYPE["Admin"]:
    app.register_blueprint(admin_views.eg001)
    app.register_blueprint(admin_views.eg002)
    app.register_blueprint(admin_views.eg003)
    app.register_blueprint(admin_views.eg004)
    app.register_blueprint(admin_views.eg005)
    app.register_blueprint(admin_views.eg006)
    app.register_blueprint(admin_views.eg007)
    app.register_blueprint(admin_views.eg008)
    app.register_blueprint(admin_views.eg009)

elif EXAMPLES_API_TYPE["Click"]:
    app.register_blueprint(click_views.eg001)
    app.register_blueprint(click_views.eg002)
    app.register_blueprint(click_views.eg003)
    app.register_blueprint(click_views.eg004)
    app.register_blueprint(click_views.eg005)
    
else:
    app.register_blueprint(esignature_views.eg001)
    app.register_blueprint(esignature_views.eg002)
    app.register_blueprint(esignature_views.eg003)
    app.register_blueprint(esignature_views.eg004)
    app.register_blueprint(esignature_views.eg005)
    app.register_blueprint(esignature_views.eg006)
    app.register_blueprint(esignature_views.eg007)
    app.register_blueprint(esignature_views.eg008)
    app.register_blueprint(esignature_views.eg009)
    app.register_blueprint(esignature_views.eg010)
    app.register_blueprint(esignature_views.eg011)
    app.register_blueprint(esignature_views.eg012)
    app.register_blueprint(esignature_views.eg013)
    app.register_blueprint(esignature_views.eg014)
    app.register_blueprint(esignature_views.eg015)
    app.register_blueprint(esignature_views.eg016)
    app.register_blueprint(esignature_views.eg017)
    app.register_blueprint(esignature_views.eg018)
    app.register_blueprint(esignature_views.eg019)
    app.register_blueprint(esignature_views.eg020)
    app.register_blueprint(esignature_views.eg022)
    app.register_blueprint(esignature_views.eg023)
    app.register_blueprint(esignature_views.eg024)
    app.register_blueprint(esignature_views.eg025)
    app.register_blueprint(esignature_views.eg026)
    app.register_blueprint(esignature_views.eg027)
    app.register_blueprint(esignature_views.eg028)
    app.register_blueprint(esignature_views.eg029)
    app.register_blueprint(esignature_views.eg030)
    app.register_blueprint(esignature_views.eg031)
    app.register_blueprint(esignature_views.eg032)
    app.register_blueprint(esignature_views.eg033)
    app.register_blueprint(esignature_views.eg034)
    app.register_blueprint(esignature_views.eg035)
    app.register_blueprint(esignature_views.eg036)
    app.register_blueprint(esignature_views.eg037)
    app.register_blueprint(esignature_views.eg038)
    app.register_blueprint(esignature_views.eg039)
    app.register_blueprint(esignature_views.eg040)


if "DYNO" in os.environ:  # On Heroku?
    import logging

    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Recipe example startup")
    app.config.update(dict(PREFERRED_URL_SCHEME="https"))

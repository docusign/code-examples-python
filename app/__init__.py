import os
from app import ds_config
from flask import Flask
from flask_wtf.csrf import CSRFProtect


session_path = "/tmp/python_recipe_sessions"

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.secret_key = ds_config.DS_CONFIG["session_secret"]
csrf = CSRFProtect(app) # See https://flask-wtf.readthedocs.io/en/stable/csrf.html

if "DYNO" in os.environ:  # On Heroku?
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Recipe example startup")
    app.config.update(dict(PREFERRED_URL_SCHEME = "https"))

from app import views

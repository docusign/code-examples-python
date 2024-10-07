#!flask/bin/python
from app import app
from flask_session import Session
import os
import sys

host = "0.0.0.0" if "--docker" in sys.argv else "localhost"
port = int(os.environ.get("PORT", 3000))

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if os.environ.get("DEBUG", False) == "True":
    app.config["DEBUG"] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.run(host=host, port=port, debug=True)
else:
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.run(host=host, port=port, extra_files="api_type.py")


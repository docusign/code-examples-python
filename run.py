#!flask/bin/python
from app import app
from flask_session import Session
import os

if os.environ.get("DEBUG", False) == "True":
    app.config["DEBUG"] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    port = int(os.environ.get("PORT", 3000))
    app.run(host="localhost", port=3000, debug=True)
else:
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.run(host="localhost", port=3000, extra_files="api_type.py")


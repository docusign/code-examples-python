#!flask/bin/python
from app import app
import os

if os.environ.get("DEBUG", False) == "True":
    app.config["DEBUG"] = True
    port = int(os.environ.get("PORT", 3000))
    app.run(host="localhost", port=3000, debug=True)
else:
    app.run(host="localhost", port=3000, extra_files="api_type.py")


#!flask/bin/python
from app import app
import os

if os.environ.get("DEBUG", False) == "True":
    app.config["DEBUG"] = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
else:
    app.run(extra_files="api_type.py")


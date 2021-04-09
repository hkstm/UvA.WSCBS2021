from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
CORS(app)

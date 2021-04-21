from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)

# app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
CORS(app)

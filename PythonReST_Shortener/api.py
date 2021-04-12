from sqlitedict import SqliteDict
from flask import Flask, request, jsonify, Blueprint
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import sqlite3
apiblue = Blueprint('api', __name__)

api = Api(apiblue)
import re

# From Django
def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

class URLGenerator(Resource):
    def get(self):
        id = request.args.get('id')

        if not id:
            return jsonify(
                {
                    "code":200,
                    "keys": mydict.keys(),
                }
            )

        if not mydict[id]:

            return jsonify(
                {
                    "code": 404,
                }
            )

        return jsonify(
            {

                "code": 301,
                "longUrl": mydict[id],

            }
        )

    def post(self):

        json_data = request.get_json(force=True)
        longUrl = json_data["longurl"]

        if not is_valid_url(longUrl):
           return jsonify(
                {
                    "code": 400,
                    "error": "invalidURL"
                }
            )

       

        count = len(mydict)
        id = count + 1

        mydict[id] = longUrl

        return jsonify(
            {

                "200": id,

            }
        )

    def put(self):
        return

    def delete(self):
        json_data = request.get_json(force=True)
        shortUrl = json_data["shorturl"]
        del mydict[shortUrl]



api.add_resource(URLGenerator, '/generator')


if __name__ == "__main__":
    app = Flask(__name__)

    app.register_blueprint(apiblue, url_prefix='/api')


    mydict = SqliteDict('./URLs.sqlite', autocommit=True)

    app.run(debug=True, port=3000, host='0.0.0.0')

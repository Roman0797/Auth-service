import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def authorize_user():
    record = json.loads(request.data)
    return jsonify(record)


app.run(debug=True)
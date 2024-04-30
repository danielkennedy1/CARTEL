from flask import Flask, request, jsonify
import hashlib
from cartel.db_setup import create_db

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hash_string():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    input_string = data.get('string')

    if input_string is None:
        return jsonify({"error": "Missing 'string' in JSON payload"}), 400

    sha1_hash = hashlib.sha1(input_string.encode())
    hash_digest = sha1_hash.hexdigest()

    return jsonify({"sha1": hash_digest})

if __name__ == '__main__':
    create_db(reset=True)
    app.run()


from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hash_string():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    # Get data from JSON
    data = request.get_json()
    input_string = data.get('string')

    # Check if the string is actually provided
    if input_string is None:
        return jsonify({"error": "Missing 'string' in JSON payload"}), 400

    # Compute the SHA-1 hash of the input string
    sha1_hash = hashlib.sha1(input_string.encode())
    hash_digest = sha1_hash.hexdigest()

    # Return the SHA-1 hash
    return jsonify({"sha1": hash_digest})

if __name__ == '__main__':
    app.run(debug=True)


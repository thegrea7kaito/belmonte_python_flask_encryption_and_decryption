from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a key and instantiate a Fernet instance
key = Fernet.generate_key()
cipher = Fernet(key)

# POST /encrypt: Encrypt a given text
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    plaintext = data.get('text')

    if not plaintext:
        return jsonify({"message": "Text is required for encryption"}), 400

    encrypted_text = cipher.encrypt(plaintext.encode())
    return jsonify({
        "original_text": plaintext,
        "encrypted_text": encrypted_text.decode()
    }), 201

# POST /decrypt: Decrypt the given encrypted text
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    encrypted_text = data.get('encrypted_text')

    if not encrypted_text:
        return jsonify({"message": "Encrypted text is required for decryption"}), 400

    try:
        decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
        return jsonify({
            "encrypted_text": encrypted_text,
            "decrypted_text": decrypted_text
        }), 200
    except Exception as e:
        return jsonify({"message": "Decryption failed", "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

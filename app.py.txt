from flask import Flask, request, jsonify
import extract_msg
import os

app = Flask(__name__)

@app.route("/parse", methods=["POST"])
def parse_msg():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        filepath = "/tmp/" + file.filename
        file.save(filepath)

        msg = extract_msg.Message(filepath)
        msg_text = msg.body

        os.remove(filepath)

        return jsonify({"text": msg_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

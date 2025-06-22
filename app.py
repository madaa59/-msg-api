from flask import Flask, request, jsonify
import extract_msg
import os

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_msg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = 'temp.msg'
    file.save(file_path)

    try:
        msg = extract_msg.Message(file_path)
        data = {
            "subject": msg.subject,
            "sender": msg.sender,
            "to": msg.to,
            "date": msg.date,
            "body": msg.body
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(file_path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

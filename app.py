from flask import Flask, request, send_from_directory, jsonify
import os, uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    if not file:
        return 'No file uploaded', 400

    ext = file.filename.rsplit('.', 1)[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    url = f"{request.host_url}img/{filename}"
    return jsonify({'url': url})

@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

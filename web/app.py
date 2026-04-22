#!/usr/bin/env python3
import os
from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def _allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/upload-map', methods=['POST'])
def api_upload_map():
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': 'Không có file'}), 400

    f = request.files['file']
    map_name = request.form.get('map_name', '').strip() or f.filename

    if f.filename == '':
        return jsonify({'ok': False, 'error': 'Chưa chọn file'}), 400

    if not _allowed(f.filename):
        return jsonify({'ok': False, 'error': 'Chỉ hỗ trợ file ảnh (png/jpg/gif/bmp/webp)'}), 400

    filename = secure_filename(f.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(save_path)

    return jsonify({'ok': True, 'filename': filename, 'map_name': map_name, 'url': f'/uploads/{filename}'})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

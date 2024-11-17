from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from .models import db, Product
from .ocr.detect_expiration import detect_expiration_date
from .utils import allowed_file
from .notifications.firebase_client import send_notification

server_bp = Blueprint('server_bp', __name__)

@server_bp.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'device_token' not in request.form:
        return jsonify({"error": "Missing image or device_token"}), 400

    image_file = request.files['image']
    device_token = request.form['device_token']

    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        expiration_date = detect_expiration_date(image_path)
        os.remove(image_path)

        if expiration_date:
            product = Product(name='Unknown Item', expiration_date=expiration_date, device_token=device_token)
            db.session.add(product)
            db.session.commit()
            return jsonify({"expiration_date": expiration_date.strftime('%Y-%m-%d')}), 200
        else:
            return jsonify({"error": "Expiration date not found"}), 404
    else:
        return jsonify({"error": "Invalid file type"}), 400

@server_bp.route('/')
def index():
    return render_template('index.html')

@server_bp.route('/upload')
def upload():
    return render_template('upload.html')

@server_bp.route('/results')
def results():
    return render_template('results.html')

@server_bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({"products": [
        {
            "name": product.name,
            "expiration_date": product.expiration_date.strftime('%Y-%m-%d'),
            "notify_date": product.notify_date.strftime('%Y-%m-%d')
        } for product in products
    ]})
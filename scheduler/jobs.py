from flask import current_app
from server.models import db, Product
from server.notifications.firebase_client import send_notification
from datetime import datetime

def check_for_notifications():
    with current_app.app_context():
        today = datetime.utcnow().date()
        products = Product.query.filter_by(notify_date=today).all()

        for product in products:
            sent = send_notification(product.name, product.expiration_date, product.device_token)
            if sent:
                print(f"Notification sent for product ID {product.id}")
            else:
                print(f"Failed to send notification for product ID {product.id}")
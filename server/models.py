from . import db
from datetime import datetime, timedelta

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='Unknown Item')
    expiration_date = db.Column(db.Date, nullable=False)
    notify_date = db.Column(db.Date, nullable=False)
    device_token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, expiration_date, device_token):
        self.name = name
        self.expiration_date = expiration_date
        self.notify_date = expiration_date - timedelta(days=7)
        self.device_token = device_token
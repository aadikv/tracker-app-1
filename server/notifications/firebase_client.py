import firebase_admin
from firebase_admin import messaging, credentials
from config import Config

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

def send_notification(product_name, expiration_date, device_token):
    message = messaging.Message(
        notification=messaging.Notification(
            title="Expiration Alert",
            body=f"The item '{product_name}' will expire on {expiration_date.strftime('%Y-%m-%d')}.",
        ),
        token=device_token
    )
    try:
        response = messaging.send(message)
        print("Notification sent:", response)
        return True
    except Exception as e:
        print("Failed to send notification:", e)
        return False
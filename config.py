import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH', os.path.join(os.getcwd(), 'expiration_tracker.db'))
    SCHEDULER_API_ENABLED = True
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS', os.path.join(os.getcwd(), 'firebase-adminsdk.json'))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
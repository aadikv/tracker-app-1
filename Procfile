release: flash db init && flask db migrate -m "Auto migration" && flask db upgrade
web: gunicorn app:app
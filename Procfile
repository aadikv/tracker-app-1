venv: python -m venv venv
install: source venv/bin/activate && pip install -r requirements.txt
release: flask db migrate -m "Auto migration" && flask db upgrade
web: python app:app
clean: rm -rf venv
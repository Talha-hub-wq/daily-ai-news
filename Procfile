release: python -c "from config.settings import validate_config; validate_config()"
web: gunicorn -w 1 -b 0.0.0.0:$PORT 'app.main:app'

from flask import Flask

# Create Flask application
application = Flask(__name__, instance_relative_config=True)

try:
    application.config.from_pyfile("production.py", silent=False)
except Exception:
    application.config.from_pyfile("production.py.cfg", silent=False)

from flask import Flask
from config import MYSQL_DB, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, SECRET_KEY

from flask_wtf.csrf import CSRFProtect

from src.flask_mysql_connector import FlaskMySQLConnector

mysql = FlaskMySQLConnector()

def create_app() -> Flask:
    """
    Factory function to create a Flask application.
    This function initializes the app, configures it, and sets up MySQL and blueprints.
    """
    # Create a Flask application instance
    app = Flask(__name__)

    # Load configuration from a config file or environment variables
    app.config.from_mapping(
        MYSQL_USER=MYSQL_USER,
        MYSQL_PASSWORD=MYSQL_PASSWORD,
        MYSQL_DB=MYSQL_DB,
        MYSQL_HOST=MYSQL_HOST,
        SECRET_KEY=SECRET_KEY
    )

    # Initialize the MySQL connection
    mysql.init_app(app)

    CSRFProtect(app)

    # Return the Flask application instance
    return app
from flask import Flask, render_template
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

    # Enable CSRF protection for the app
    CSRFProtect(app)

    from .routes import students_bp, programs_bp, colleges_bp
    # Register Blueprints
    app.register_blueprint(students_bp, url_prefix='/students')  # URL prefix for students
    print("Loading students...")
    app.register_blueprint(programs_bp, url_prefix='/programs')  # URL prefix for programs
    print("Loading students...")
    app.register_blueprint(colleges_bp, url_prefix='/colleges')  # URL prefix for colleges
    print("Loading students...")

    # Register any other Blueprints or route modules here as needed

    # Create a root index route (optional)
    @app.route('/')
    def index() -> str:
        return render_template('tabs.html')  # Render the main tabbed view

    # Return the Flask application instance
    return app
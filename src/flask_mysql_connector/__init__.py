from typing import Optional

from flask import Flask, current_app, g

from mysql.connector import Error
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract

import mysql.connector

ctx = g

class FlaskMySQLConnector:
    def __init__(self, app: Optional[Flask] = None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Flask) -> None:
        # Set default MySQL configurations if not already provided
        app.config.setdefault("MYSQL_HOST", "localhost")
        app.config.setdefault("MYSQL_PORT", 3306)
        app.config.setdefault("MYSQL_USER", "root")
        app.config.setdefault("MYSQL_PASSWORD", "")
        app.config.setdefault("MYSQL_DB", "")

        # Register teardown function to close DB connections after request
        app.teardown_appcontext(self.teardown)

    @property
    def connect(self) -> PooledMySQLConnection | MySQLConnectionAbstract:
        """
        Establishes a new MySQL database connection using the Flask app's configuration.

        Returns:
            mysql.connector.connection.MySQLConnection: A MySQL connection object.
        """
        try:
            connection = mysql.connector.connect(
                host=current_app.config["MYSQL_HOST"],
                port=current_app.config["MYSQL_PORT"],
                user=current_app.config["MYSQL_USER"],
                password=current_app.config["MYSQL_PASSWORD"],
                database=current_app.config["MYSQL_DB"]
            )
            return connection
        except Error as e:
            current_app.logger.error(f"Error connecting to MySQL: {e}")
            raise e
    
    @property
    def connection(self) -> PooledMySQLConnection | MySQLConnectionAbstract:
        """
        Retrieves or creates a MySQL database connection for the current Flask request context.

        Returns:
            mysql.connector.connection.MySQLConnection: The MySQL connection object.
        """
        if "db_connection" not in ctx:
            ctx.db_connection = self.connect
        return ctx.db_connection

    def teardown(self, exception: Optional[BaseException] = None) -> None:
        connection: Optional[PooledMySQLConnection | MySQLConnectionAbstract] = ctx.pop("db_connection", None)
        if connection is not None:
            connection.close()
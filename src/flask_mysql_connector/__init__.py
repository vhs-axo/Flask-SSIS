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
    
    def teardown(self, exception: Optional[BaseException] = None) -> None:
        connection: Optional[PooledMySQLConnection | MySQLConnectionAbstract] = ctx.pop("db_connection", None)
        if connection is not None:
            connection.close()
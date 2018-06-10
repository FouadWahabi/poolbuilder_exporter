#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy import event


#################################################################################
#################################################################################
#
# Database manager: creating, backing up and switching databases
#
# --------------------------------------------------------------------------------


class Database:
    connections = {}

    def __init__(self, host, port, username, password, db_name, dialect):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.dialect = dialect

    def build_connection_string(self):
        str = '{5}://{0}:{1}@{2}:{3}/{4}'.format(self.username, self.password,
                                                 self.host,
                                                 self.port, self.db_name, self.dialect)
        return str

    def create_engine(self):
        connection_string = self.build_connection_string()
        db = create_engine(connection_string, pool_recycle=3600)

        return db

    def connect(self):
        conn_str = self.build_connection_string()
        if Database.connections.get(conn_str):
            return Database.connections[conn_str]

        db = self.create_engine()
        connection = db.connect()

        Database.connections[conn_str] = db, connection

        return db, connection

from sqlalchemy import *


class HBModels:
    def __init__(self, db):
        self.articles = Table('content_item', db, autoload=True)
        self.newsletters= Table('newsletter', db, autoload=True)

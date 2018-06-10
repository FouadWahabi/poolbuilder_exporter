from sqlalchemy import *


class PBModels:
    def __init__(self, db):
        self.source_domain = Table('source_domain', db, autoload=True)

        self.source_domain_content_directory = Table('source_domain_content_directory', db, autoload=True)

        self.content_pool = Table('content_pool', db, autoload=True)

        self.link_source_domain_to_content_pool = Table('link_source_domain_to_content_pool', db, autoload=True)

        self.settings = Table('settings', db, autoload=True)

        self.source_domain_social_links = Table('source_domain_social_links', db, autoload=True)

        self.source_domain_parsing_dict = Table('source_domain_parsing_dict', db, autoload=True)

        self.articles = Table('articles', db, autoload=True)

        self.articles_social_data = Table('articles_social_data', db, autoload=True)

        self.link_articles_social_data_to_articles = Table('link_articles_social_data_to_articles', db, autoload=True)

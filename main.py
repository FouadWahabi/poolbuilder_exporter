import logging

from sqlalchemy import MetaData

from config import *
from db.database import Database
from db.hbot_models import HBModels
from db.poolbuilder_models import PBModels
from services.hb_service import HBService
from services.pb_service import PBService


def setupLogger():
    # create logger with 'spam_application'
    logger = logging.getLogger('poolbuilder_exporter')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('poolbuilder_exporter.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


if __name__ == '__main__':

    logger = setupLogger()

    # Connect to databases

    pb_db, pb_master = Database(DB_PB_HOST, DB_PB_PORT, DB_PB_USERNAME, DB_PB_PASS, DB_PB_MASTER,
                                DB_PB_DIALECT).connect()
    hb_db, hb_master = Database(DB_HB_HOST, DB_HB_PORT, DB_HB_USERNAME, DB_HB_PASS, DB_HB_MASTER,
                                DB_HB_DIALECT).connect()

    pb_models = PBModels(MetaData(bind=pb_db))
    hb_models = HBModels(MetaData(bind=hb_db))

    # Create services

    pb_service = PBService(pb_models)
    hb_service = HBService(hb_models)

    # Find all the new articles that are not exported yet

    articles_to_export = pb_service.find_new_articles()

    for article in articles_to_export:
        if not hb_service.article_exists(article.url):
            source_id = hb_service.source_exists(article.url)
            if not source_id:
                source_id = hb_service.insert_source(article.url)
            rs = hb_service.insert_article(article, source_id)
            if rs:
                logger.info("Inserted article {0}".format(article.title))
            # Update article flag_exported and exported_date
            rs = pb_service.set_article_exported(article.id)
            if rs:
                logger.info("Set exported article {0}".format(article.title))
        else:
            logger.error("Article {0} already exists".format(article.title))

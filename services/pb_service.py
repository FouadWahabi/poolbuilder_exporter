from datetime import datetime

from sqlalchemy import or_


class PBService:
    def __init__(self, pb_models):
        self.pb_models = pb_models
        pass

    def find_all_articles(self):
        s = self.pb_models.articles.select()
        rs = s.execute()
        return rs

    def find_new_articles(self):
        articles = self.pb_models.articles
        s = articles.select().where(or_(articles.c.flag_ignore is None, articles.c.flag_ignore != True)).where(
            articles.c.flag_specific_parsed_true == True).where(
            or_(articles.c.flag_exported is None, articles.c.flag_exported != True))
        rs = s.execute()
        return rs

    def set_article_exported(self, id):
        articles = self.pb_models.articles
        s = articles.update().where(articles.c.id == id).values(flag_exported=True, date_exported=datetime.now())
        rs = s.execute()
        return rs

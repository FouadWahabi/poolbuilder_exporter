from tldextract import tldextract


class HBService:
    def __init__(self, hb_models):
        self.hb_models = hb_models
        pass

    def source_exists(self, url):
        newsletters = self.hb_models.newsletters
        s = newsletters.select().where(newsletters.c.name == self.extractname(url))
        rs = s.execute().fetchone()
        return rs[0] if rs is not None else False

    def article_exists(self, url):
        articles = self.hb_models.articles
        s = articles.select().where(articles.c.url == url)
        return s.execute().fetchone() is not None

    def extractname(self, url):
        # return url.split("//")[-1].split("/")[0].split('?')[0]
        ext = tldextract.extract(url)
        # ext is a dict that contains subdomain,domain and suffix
        result = '.'.join(ext)
        return result

    def insert_article(self, article, newsletter):
        articles = self.hb_models.articles
        s = articles.insert().values(url=article.url, newsletter=newsletter, short_url=article.url,
                                     title=article.title, abstract=article.content,
                                     date=str(article.date_modified), subject=article.abstract,
                                     status='imported', article_title=article.title, article_abstract=article.content,
                                     article_authors=[article.author], article_publish_date=str(article.published),
                                     scrapped_date=str(article.date_modified), article_tags=[article.tags],
                                     article_keywords=[], published_date=str(article.date_modified))
        try:
            rs = s.execute()
            if rs and rs.rowcount > 1:
                rs = rs.fetchall()[0]

            return rs
        except Exception:
            pass
        return None

    def insert_source(self, url):
        source = self.extractname(url)
        newsletters = self.hb_models.newsletters
        s = newsletters.insert().values(name=source, email=source, alias=source, method='')
        rs = s.execute()
        if rs and rs.rowcount > 1:
            rs = rs.fetchall()[0]
        return rs

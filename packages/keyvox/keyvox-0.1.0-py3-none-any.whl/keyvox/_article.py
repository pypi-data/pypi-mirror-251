class Article:
    def __init__(self, keyvox_instance):
        self.keyvox_instance = keyvox_instance
        self.base_url = self.keyvox_instance.base_url

    def list(self, page=1, limit=3):
        request_url = '/articles'
        complete_url = self.base_url + request_url
        articles = self.keyvox_instance.fetch_data(
            complete_url,
            params={'page': page, 'limit': limit}
        )
        return articles

    def get_by_id(self, article_id: str):
        request_url = '/articles/' + str(article_id)
        complete_url = self.base_url + request_url
        params = {}
        article = self.keyvox_instance.fetch_data(
            url=complete_url,
            params=params
        )
        return article

    def get_by_slug(self, slug: str):
        request_url = '/articles/' + str(slug)
        complete_url = self.base_url + request_url
        params = {}
        article = self.keyvox_instance.fetch_data(
            url=complete_url,
            params=params
        )
        return article

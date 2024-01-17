class Tag():
    def __init__(self, keyvox_instance):
        self.keyvox_instance = keyvox_instance
        self.base_url = self.keyvox_instance.base_url

    def list(self):
        request_url = '/tags'
        complete_url = self.base_url + request_url
        tags = self.keyvox_instance.fetch_data(
            complete_url,
            params={}
        )
        return tags

    def get_by_slug(self, tag_slug: str):
        request_url = '/tags/' + str(tag_slug)
        complete_url = self.base_url + request_url
        params = {}
        tag = self.keyvox_instance.fetch_data(
            url=complete_url,
            params=params
        )
        return tag

    def get_by_article_slug(self, article_id: str):
        request_url = '/tags/' + str(article_id)
        complete_url = self.base_url + request_url
        params = {}
        tags = self.keyvox_instance.fetch_data(
            url=complete_url,
            params=params
        )
        return tags

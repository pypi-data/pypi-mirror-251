from requests import get, Response
from keyvox._article import Article
from keyvox._tag import Tag


class KeyVox:
    def __init__(self, api_key: str, base_url='https://keyvox.dev/api'):
        self.api_key = api_key
        self.base_url = base_url
        self.articles = Article(self)
        self.tags = Tag(self)

    def fetch_data(self, url: str, params) -> Response:
        response = get(
            url=url,
            headers={
                'key': self.api_key
            },
            params=params
        )
        return response.json()

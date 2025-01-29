import requests
from tabnews_api_types import GetContentParams

class TabNewsRequester:
    def __init__(self):
        self.base_url = 'https://www.tabnews.com.br/api/v1'

    def get_content(self, params: GetContentParams):
        url = f"{self.base_url}/contents"
        response = requests.get(url, params={'page': params.page, 'per_page': params.per_page, 'strategy': params.strategy})
        response.raise_for_status()
        return response
import os
import requests


class SuggestionService:
    endpoint = os.getenv('SUGGESTOIN_BASE_URL')

    @classmethod
    def get_suggested_category_id(cls, product_name, product_features):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        request_body = {
            'name': product_name,
            'features': product_features,
        }
        result = requests.post(cls.endpoint + '/product/suggest-category/',
                               json=request_body,
                               headers=headers)
        return result.json()['id']

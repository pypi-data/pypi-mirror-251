import requests
from docketanalyzer.utils import COURTLISTENER_TOKEN


class RECAPApi:
    def __init__(self, token=None):
        if token is None:
            token = COURTLISTENER_TOKEN
        self.token = token
        self.headers = {'Authorization': f'Token {self.token}'}
        self.base_url = 'https://www.courtlistener.com/api/rest/v3/'
        self.endpoint_ordering = {
            'docket-entries': 'date_created',
            'parties': 'date_created',
            'attorneys': 'date_created',
        }

    def make_request(self, endpoint, params={}):
        if 'order_by' not in params and endpoint in self.endpoint_ordering:
            params['order_by'] = self.endpoint_ordering[endpoint]
        url = self.base_url + endpoint
        r = requests.get(url, params=params, headers=self.headers)
        return r.json()

    def make_paginated_request(self, endpoint, params={}, max_depth=49):
        r = self.make_request(endpoint, params=params)
        next = r['next']
        data = r['results']
        total_page, page = 1, 1
        while next:
            if page >= max_depth:
                ordering = self.endpoint_ordering[endpoint]
                params[f"{ordering}__gte"] = data[-1][ordering]
                r = self.make_request(endpoint, params=params)
                page = 0
            else:
                r = requests.get(next, headers=self.headers).json()
            next = r['next']
            data += r['results']
            page += 1
            total_page += 1
            print(f'page {total_page} collected')
        deduped_data, ids = [], []
        for row in data:
            if row['id'] not in ids:
                deduped_data.append(row)
                ids.append(row['id'])
        return deduped_data

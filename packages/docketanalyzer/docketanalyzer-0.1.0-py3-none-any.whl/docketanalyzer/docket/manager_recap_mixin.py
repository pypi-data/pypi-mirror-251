from datetime import datetime
import requests
import simplejson as json
from docketanalyzer import RECAPApi


class RECAPMixin:
    @property
    def recap_ids(self):
        return [int(path.stem.split('.')[-1]) for path in self.recap_docket_paths]

    @property
    def recap_docket_paths(self):
        return self.dir.glob('recap.dockets.*.json')

    @property
    def recap_entry_paths(self):
        return self.dir.glob('recap.docket-entries.*.json')

    @property
    def recap_docket_jsons(self):
        return [json.loads(path.read_text()) for path in self.recap_docket_paths]

    @property
    def recap_entry_jsons(self):
        return [json.loads(path.read_text()) for path in self.recap_entry_paths]

    def recap_download_dockets(self):
        api = RECAPApi()
        print(f'downloading dockets for {self.docket_id}')
        params = {
            'court__id': self.docket.court.name,
            'docket_number': self.docket.docket_number
        }
        data = api.make_paginated_request('dockets', params=params)
        for row in data:
            row['downloaded_at'] = str(datetime.now())
            path = self.dir / f"recap.dockets.{row['id']}.json"
            path.write_text(json.dumps(row, indent=4))

    def recap_download_resource(self, endpoint, recap_id=None):
        recap_ids = self.recap_ids if recap_id is None else [recap_id]
        api = RECAPApi()
        for recap_id in recap_ids:
            out_path = self.dir / f"recap.{endpoint}.{recap_id}.json"
            print(f'downloading {endpoint} for {self.docket_id} (recap {recap_id})')
            data = api.make_paginated_request(
                endpoint,
                params={'docket__id': recap_id},
            )
            data = {
                'data': data,
                'downloaded_at': str(datetime.now()),
            }
            out_path.write_text(json.dumps(data, indent=4))

    def recap_download_entries(self, recap_id=None):
        self.recap_download_resource('docket-entries', recap_id=recap_id)

    def recap_download_parties(self, recap_id=None):
        self.recap_download_resource('parties', recap_id=recap_id)

    def recap_download_attorneys(self, recap_id=None):
        self.recap_download_resource('attorneys', recap_id=recap_id)

    def recap_download_documents(self, recap_id=None):
        recap_ids = self.recap_ids if recap_id is None else [recap_id]
        for recap_id in recap_ids:
            entries_path = self.dir / f"recap.docket-entries.{recap_id}.json"
            if entries_path.exists():
                entries = json.loads(entries_path.read_text())['data']
                for entry in entries:
                    for doc in entry['recap_documents']:
                        if doc['filepath_ia'] or doc['filepath_local']:
                            attachment_number = doc['attachment_number']
                            pdf_path = self.document_get_pdf_path(
                                entry['entry_number'], attachment_number,
                            )
                            ocr_path = self.document_get_ocr_path(
                                entry['entry_number'], attachment_number,
                            )

                            if not pdf_path.exists():
                                if doc['filepath_ia']:
                                    url = doc['filepath_ia']
                                else:
                                    url = 'https://storage.courtlistener.com/recap/'
                                    url += doc['filepath_local'].split('recap/')[-1]
                                pdf_path.write_bytes(requests.get(url).content)

                            if pdf_path.exists():
                                if not ocr_path.exists() and 'plain_text' in doc:
                                    ocr_data = {
                                        'content': doc['plain_text'],
                                        'page_count': doc['page_count'],
                                    }
                                    ocr_path.write_text(json.dumps(ocr_data, indent=4))

    def recap_update(self, recap_id=None):
        if recap_id is None:
            self.recap_download_dockets()
        self.recap_download_entries(recap_id)
        self.recap_download_parties(recap_id)
        self.recap_download_attorneys(recap_id)
        self.recap_download_documents(recap_id)

    def recap_consolidate_header(self):
        data = []
        for recap_docket in self.recap_docket_jsons:
            row = {
                'court': recap_docket['court_id'],
                'filing_date': recap_docket['date_filed'],
                'terminating_date': recap_docket['date_terminated'],
                'cause': recap_docket['cause'],
            }
            nature_suit = recap_docket['nature_of_suit'].split()[0]
            if nature_suit.isdigit():
                row['nature_suit'] = f"_{nature_suit}"
            data.append(row)
        return data

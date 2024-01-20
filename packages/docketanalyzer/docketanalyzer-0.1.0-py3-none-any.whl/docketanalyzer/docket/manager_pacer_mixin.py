import simplejson as json


class PACERMixin:
    @property
    def pacer_html_paths(self):
        return self.dir.glob('pacer.*.html')

    @property
    def pacer_json_path(self):
        return self.dir / 'pacer.json'

    @property
    def pacer_json(self):
        if self.pacer_json_path.exists():
            return json.loads(self.pacer_json_path.read_text())
        print(f'No pacer.json for {self.dir}')

    def pacer_add_html(self, html):
        path = self.dir / f'pacer.{len(list(self.html_paths))}.html'
        path.write_text(html)

    def pacer_consolidate_header(self):
        pacer_json = self.pacer_json
        if pacer_json is not None:
            pacer_json['docket_number'] = pacer_json['ucid'].split(';;')[-1]
            pacer_json['nature_suit'] = f"_{pacer_json['nature_suit'].split()[0]}"
            fields = [
                'court', 'docket_number', 'filing_date', 'terminating_date',
                'nature_suit', 'cause'
            ]
            return {k: pacer_json[k] for k in fields}
        return {}

    def pacer_consolidate_entries(self):
        pacer_json = self.pacer_json
        entries = []
        if pacer_json is not None:
            for row_number, entry in enumerate(pacer_json['docket']):
                docs = []
                for attachment_number, doc in entry['documents'].items():
                    attachment_number = int(attachment_number)
                    attachment_number = None if attachment_number == 0 else attachment_number
                    docs.append({
                        'attachment_number': attachment_number,
                        'pacer_url': doc['url'],
                    })
                entries.append({
                    'row_number': row_number,
                    'entry_number': entry['ind'],
                    'text': entry['docket_text'],
                    'date_filed': entry['date_filed'],
                    'docs': docs,
                })
        return entries

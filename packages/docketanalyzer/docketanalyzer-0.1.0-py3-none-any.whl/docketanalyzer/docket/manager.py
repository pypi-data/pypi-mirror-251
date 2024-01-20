from datetime import datetime
from pathlib import Path
import simplejson as json
from docketanalyzer.docket.manager_document_mixin import DocumentMixin
from docketanalyzer.docket.manager_pacer_mixin import PACERMixin
from docketanalyzer.docket.manager_idb_mixin import IDBMixin
from docketanalyzer.docket.manager_recap_mixin import RECAPMixin
from docketanalyzer.utils import DATA_DIR


class DocketManager(
    DocumentMixin, PACERMixin,
    IDBMixin, RECAPMixin,
):
    def __init__(self, docket_id: str, data_dir: [str, Path] = DATA_DIR) -> None:
        self.docket_id = docket_id
        self.data_dir = Path(data_dir)
        self.cache = {}

    @property
    def dir(self):
        return self.data_dir / 'dockets' / 'data' / self.docket_id

    def consolidate(self):
        data = {'id': self.docket_id, **self.pacer_consolidate_header()}

        for recap_header in self.recap_consolidate_header():
            for k, v in recap_header.items():
                if (k not in data or data[k] is None) and v is not None:
                    data[k] = v

        data['entries'] = self.pacer_consolidate_entries()
        data['idb'] = self.idb_consolidate()
        return data

    def consolidate_and_save(self):
        from .docket import Docket
        data = Docket(**self.consolidate()).to_dict()
        self.docket_json_path.write_text(json.dumps(data, indent=4))
        self.set_status('consolidated_at', str(datetime.now()))

    @property
    def docket_json_path(self):
        return self.dir / 'docket.json'

    @property
    def docket(self):
        if 'docket' not in self.cache:
            if not self.docket_json_path.exists():
                self.consolidate_and_save()
            from .docket import Docket
            self.cache['docket'] = Docket.from_dict(json.loads(self.docket_json_path.read_text()))
        return self.cache['docket']

    @property
    def status_path(self):
        return self.dir / 'status.json'

    @property
    def status(self):
        if self.status_path.exists():
            return json.loads(self.status_path.read_text())
        return {}

    def set_status(self, k, v):
        status = self.status
        status[k] = v
        self.status_path.write_text(json.dumps(status, indent=4))

    def delete_status(self, k):
        status = self.status
        if k in status:
            del status[k]
            self.status_path.write_text(json.dumps(status, indent=4))

    @property
    def unexpected_files(self):
        return [
            path for path in self.dir.iterdir() if
            not path.name.startswith('.') and
            not any(
                path.name.startswith(prefix + '.')
                for prefix in ['docket', 'doc', 'status', 'pacer', 'recap', 'idb']
            )
        ]

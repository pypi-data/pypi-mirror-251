from datetime import datetime
from typing import Optional, Union
import pandas as pd
from .document import Document


class DocketEntry:
    def __init__(
        self,
        docket: 'Docket',
        row_number: int,
        text: str,
        date_filed: Union[str, datetime],
        entry_number: Optional[int] = None,
        docs: list[dict] = [],
        **kwargs,
    ):
        self.docket = docket
        self.row_number = row_number
        self.text = text
        self.date_filed = pd.to_datetime(date_filed) if isinstance(date_filed, str) else date_filed
        self.entry_number = entry_number
        self.docs = [Document(entry=self, **x) for x in docs]

    @property
    def id(self):
        return f'{self.docket.id}__{self.row_number}'

    def to_dict(self):
        docs = [x.to_dict() for x in self.docs]
        return {
            'row_number': self.row_number,
            'text': self.text,
            'date_filed': str(self.date_filed.date()),
            'entry_number': self.entry_number,
            'docs': docs,
        }

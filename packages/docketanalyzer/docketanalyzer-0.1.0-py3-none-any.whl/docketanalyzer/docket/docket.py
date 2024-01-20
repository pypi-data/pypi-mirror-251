from datetime import datetime
from pathlib import Path
from typing import Optional, Union
import pandas as pd
from docketanalyzer.categories import (
    CaseType,
    DistrictCourt,
    NatureSuit,
)
from docketanalyzer.utils import DATA_DIR
from .entry import DocketEntry
from .idb_entry import IDBEntry
from .manager import DocketManager


class Docket:
    def __init__(
        self, id: str,
        filing_date: Optional[Union[str, datetime.date]] = None,
        terminating_date: Optional[Union[str, datetime.date]] = None,
        nature_suit: Optional[Union[str, NatureSuit]] = None,
        cause: Optional[str] = None,
        entries: list[dict] = [],
        idb: list[dict] = [],
        data_dir: [str, Path] = DATA_DIR,
        manager: Optional[DocketManager] = None,
        **kwargs,
    ) -> None:
        self.id = id
        self.manager = DocketManager(self.id, data_dir) if manager is None else manager

        court_id, docket_number = id.split('__')
        docket_number = docket_number.replace('_', ':')
        self.court = DistrictCourt[court_id]
        self.docket_number = docket_number
        docket_parts = self.docket_number.split('-')
        self.docket_office = docket_parts[0].split(':')[0]
        self.docket_year = docket_parts[0].split(':')[1]
        self.case_type = CaseType[docket_parts[1]]
        self.filing_number = docket_parts[2]
        self.filing_date = pd.to_datetime(filing_date).date() if isinstance(filing_date, str) else filing_date
        self.terminating_date = pd.to_datetime(terminating_date).date() if isinstance(terminating_date, str) else terminating_date
        self.nature_suit = NatureSuit[nature_suit] if isinstance(nature_suit, str) else nature_suit
        self.cause = cause
        self.entries = [DocketEntry(docket=self, **x) for x in entries]
        self.idb = [IDBEntry(docket=self, **x) for x in idb]

    def to_dict(self):
        entries = [x.to_dict() for x in self.entries]
        idb = [x.to_dict() for x in self.idb]
        return {
            'id': self.id,
            'court': self.court.name,
            'docket_number': self.docket_number,
            'docket_office': self.docket_office,
            'docket_year': self.docket_year,
            'case_type': self.case_type.name,
            'filing_number': self.filing_number,
            'filing_date': str(self.filing_date) if self.filing_date else None,
            'terminating_date': str(self.terminating_date) if self.terminating_date else None,
            'nature_suit': self.nature_suit.name if self.nature_suit else None,
            'cause': self.cause,
            'entries': entries,
            'idb': idb,
        }

    @staticmethod
    def from_dict(data: dict):
        return Docket(**data)

    @staticmethod
    def from_id(docket_id: str, data_dir: [str, Path] = DATA_DIR):
        manager = DocketManager(docket_id, data_dir)
        return manager.docket

    @staticmethod
    def create_id(court_id: str, docket_number: str):
        return f"{court_id}__{docket_number.replace(':', '_')}"

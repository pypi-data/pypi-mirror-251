from datetime import datetime
from typing import Union
import pandas as pd
from docketanalyzer.categories import (
    IDBArbitrationAtFiling,
    IDBArbitrationAtTermination,
    IDBClassAction,
    IDBDisposition,
    IDBIFP,
    IDBJudgment,
    IDBMDL,
    IDBNatureOfJudgment,
    IDBOrigin,
    IDBProceduralProgress,
    IDBProSe,
    IDBStatusCode,
)


class IDBEntry:
    def __init__(
        self,
        docket: 'Docket',
        idb_index: int,
        filing_date: Union[str, datetime.date],
        terminating_date: Union[str, datetime.date],
        arbitration_at_filing: Union[IDBArbitrationAtFiling, str],
        arbitration_at_termination: Union[IDBArbitrationAtTermination, str],
        class_action: Union[IDBClassAction, str],
        disposition: Union[IDBDisposition, str],
        ifp: Union[IDBIFP, str],
        judgment: Union[IDBJudgment, str],
        mdl: Union[IDBMDL, str],
        nature_of_judgment: Union[IDBNatureOfJudgment, str],
        origin: Union[IDBOrigin, str],
        pro_se: Union[IDBProSe, str],
        procedural_progress: Union[IDBProceduralProgress, str],
        status_code: Union[IDBStatusCode, str],
        **kwargs,
    ):
        self.docket = docket
        self.idb_index = idb_index
        self.filing_date = pd.to_datetime(filing_date).date() if isinstance(filing_date, str) else filing_date
        self.terminating_date = pd.to_datetime(terminating_date).date() if isinstance(terminating_date, str) else terminating_date
        self.arbitration_at_filing = IDBArbitrationAtFiling[arbitration_at_filing] if isinstance(arbitration_at_filing, str) else arbitration_at_filing
        self.arbitration_at_termination = IDBArbitrationAtTermination[arbitration_at_termination] if isinstance(arbitration_at_termination, str) else arbitration_at_termination
        self.class_action = IDBClassAction[class_action] if isinstance(class_action, str) else class_action
        self.disposition = IDBDisposition[disposition] if isinstance(disposition, str) else disposition
        self.ifp = IDBIFP[ifp] if isinstance(ifp, str) else ifp
        self.judgment = IDBJudgment[judgment] if isinstance(judgment, str) else judgment
        self.mdl = IDBMDL[mdl] if isinstance(mdl, str) else mdl
        self.nature_of_judgment = IDBNatureOfJudgment[nature_of_judgment] if isinstance(nature_of_judgment, str) else nature_of_judgment
        self.origin = IDBOrigin[origin] if isinstance(origin, str) else origin
        self.pro_se = IDBProSe[pro_se] if isinstance(pro_se, str) else pro_se
        self.procedural_progress = IDBProceduralProgress[procedural_progress] if isinstance(procedural_progress, str) else procedural_progress
        self.status_code = IDBStatusCode[status_code] if isinstance(status_code, str) else status_code

    def to_dict(self):
        return {
            'idb_index': self.idb_index,
            'filing_date': str(self.filing_date),
            'terminating_date': str(self.terminating_date),
            'arbitration_at_filing': self.arbitration_at_filing.name,
            'arbitration_at_termination': self.arbitration_at_termination.name,
            'class_action': self.class_action.name,
            'disposition': self.disposition.name,
            'ifp': self.ifp.name,
            'judgment': self.judgment.name,
            'mdl': self.mdl.name,
            'nature_of_judgment': self.nature_of_judgment.name,
            'origin': self.origin.name,
            'pro_se': self.pro_se.name,
            'procedural_progress': self.procedural_progress.name,
            'status_code': self.status_code.name,
        }

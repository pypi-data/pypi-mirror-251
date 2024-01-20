import pandas as pd
import simplejson as json
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
from docketanalyzer import load_elastic


fields = {
    'origin': {
        'col': 'ORIGIN',
        'cat': IDBOrigin,
        'mapping': {
            '1': 'Original Proceeding',
            '2': 'Removed',
            '3': 'Remanded for Further Action',
            '4': 'Reinstated/Reopened',
            '5': 'Transferred from Another District',
            '6': 'Multi District Litigation',
            '7': 'Appeal to District Judge of Magistrate Judge Decision',
            '8': 'Second Reopen',
            '9': 'Third Reopen',
            '10': 'Fourth Reopen',
            '11': 'Fifth Reopen',
            '12': 'Sixth Reopen',
            '13': 'Multi District Litigation Originating in the District',
        },
    },

    'procedural_progress': {
        'col': 'PROCPROG',
        'cat': IDBProceduralProgress,
        'mapping': {
            '1': 'Before Issue Joined - No Court Action',
            '2': 'Before Issue Joined - Order Entered',
            '11': 'Before Issue Joined - Hearing Held',
            '12': 'Before Issue Joined - Order Decided',
            '3': 'After Issue Joined - No Court Action',
            '4': 'After Issue Joined - Judgment on Motion',
            '5': 'After Issue Joined - Pretrial Conference Held',
            '6': 'After Issue Joined - During Court Trial',
            '7': 'After Issue Joined - During Jury Trial',
            '8': 'After Issue Joined - After Court Trial',
            '9': 'After Issue Joined - After Jury Trial',
            '10': 'After Issue Joined - Other',
            '13': 'After Issue Joined - Request for Trial De Novo After Arbitration',
            '-8': 'Missing',
        },
    },

    'disposition': {
        'col': 'DISP',
        'cat': IDBDisposition,
        'mapping': {
            '0': 'Transfer to Another District',
            '1': 'Remanded to State Court',
            '10': 'Multi District Litigation Transfer',
            '11': 'Remanded to U.S. Agency',
            '2': 'Dismissal - Want of Prosecution',
            '3': 'Dismissal - Lack of Jurisdiction',
            '12': 'Dismissal - Voluntarily',
            '13': 'Dismissal - Settled',
            '14': 'Dismissal - Other',
            '4': 'Judgment on Default',
            '5': 'Judgment on Consent',
            '6': 'Judgment on Motion Before Trial',
            '7': 'Judgment on Jury Verdict',
            '8': 'Judgment on Directed Verdict',
            '9': 'Judgment on Court Trial',
            '15': 'Judgment on Award of Arbitrator',
            '16': 'Stayed Pending Bankruptcy',
            '17': 'Other',
            '18': 'Statistical Closing',
            '19': 'Appeal Affirmed (Magistrate Judge)',
            '20': 'Appeal Denied (Magistrate Judge)',
            '-8': 'Missing',
        },
    },

    'pro_se': {
        'col': 'PROSE',
        'cat': IDBProSe,
        'mapping': {
            '0': 'None',
            '1': 'Plaintiff',
            '2': 'Defendant',
            '3': 'Both Plaintiff & Defendant',
            '-8': 'Missing',
        },
    },

    'judgment': {
        'col': 'JUDGMENT',
        'cat': IDBJudgment,
        'mapping': {
            '1': 'Plaintiff',
            '2': 'Defendant',
            '3': 'Both',
            '4': 'Unknown',
            '0': 'Missing',
            '-8': 'Missing',
        },
    },

    'nature_of_judgment': {
        'col': 'NOJ',
        'cat': IDBNatureOfJudgment,
        'mapping': {
            '0': 'No Monetary Award',
            '1': 'Monetary Award Only',
            '2': 'Monetary Award and Other',
            '3': 'Injunction',
            '4': 'Forfeiture/Foreclosure/Condemnation, etc.',
            '5': 'Costs Only',
            '6': 'Costs and Attorney Fees',
            '-8': 'Missing',
        },
    },

    'status_code': {
        'col': 'STATUSCD',
        'cat': IDBStatusCode,
        'mapping': {
            'S': 'Pending Record',
            'L': 'Terminated Record',
            'nan': 'Missing',
            'None': 'Missing',
        },
    },

    'arbitration_at_filing': {
        'col': 'ARBIT',
        'cat': IDBArbitrationAtFiling,
        'mapping': {
            'M': 'Mandatory',
            'V': 'Voluntary',
            'E': 'Exempt',
            'Y': 'Yes, Type Unknown',
            'N': 'No',
            '-8': 'Missing',
        },
    },

    'arbitration_at_termination': {
        'col': 'TRMARB',
        'cat': IDBArbitrationAtTermination,
        'mapping': {
            'M': 'Mandatory',
            'V': 'Voluntary',
            'E': 'Exempt',
            '-8': 'Missing',
        },
    },
}


class IDBMixin:
    @property
    def idb_entry_paths(self):
        return self.dir.glob('idb.*.json')

    @property
    def idb_entries(self):
        return [json.loads(x.read_text()) for x in self.idb_entry_paths]

    def idb_update(self):
        es = load_elastic()
        idb_entries = es.search(
            index="idb", 
            body={"query": {"match": {'docket_id': self.docket_id}}}
        )['hits']['hits']

        if not idb_entries:
            filing_date = self.docket.filing_date
            if filing_date:
                filing_date = filing_date.date().strftime("%m/%d/%Y")
                weak_docket_id = self.docket.court.name + '_' + self.docket.docket_number.split(':')[-1] + '_' + filing_date
                idb_entries = es.search(
                    index="idb", 
                    body={"query": {"match": {'weak_docket_id': weak_docket_id}}}
                )['hits']['hits']
                if idb_entries:
                    matched_docket_id = idb_entries[-1]['_source']['docket_id']
                    idb_entries = es.search(
                        index="idb", 
                        body={"query": {"match": {'docket_id': matched_docket_id}}}
                    )['hits']['hits']

        for path in self.idb_entry_paths:
            path.unlink()

        if idb_entries:
            idb_entries = [x['_source'] for x in idb_entries]
            for idb_entry in idb_entries:
                path = self.dir / f'idb.{idb_entry["id"]}.json'
                path.write_text(json.dumps(idb_entry, indent=4))
        es.transport.close()

    def idb_consolidate(self):
        data = []
        for idb_entry in self.idb_entries:
            row = {'idb_index': idb_entry['id']}
            idb_entry = json.loads(idb_entry['data'])
            row['filing_date'] = pd.to_datetime(idb_entry['FILEDATE']).date()
            row['terminating_date'] = pd.to_datetime(idb_entry['TERMDATE']).date()
            row['ifp'] = IDBIFP('Yes' if idb_entry['IFP'] != '-8' else 'No').name
            row['mdl'] = IDBMDL('Yes' if str(idb_entry['MDLDOCK']) != '-8' else 'No').name
            row['class_action'] = IDBClassAction('Yes' if str(idb_entry['CLASSACT']) != '-8' else 'No').name
            for field_name, field in fields.items():
                v = idb_entry[field['col']]
                if v is not None:
                    v = field['cat'](field['mapping'][v]).name
                row[field_name] = v
            data.append(row)
        return data

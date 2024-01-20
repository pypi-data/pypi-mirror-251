from typing import Optional
import simplejson as json


class Document:
    def __init__(
        self,
        entry: 'DocketEntry',
        attachment_number: Optional[int] = None,
        pacer_url: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs,
    ):
        self.entry = entry
        self.attachment_number = attachment_number
        self.pacer_url = pacer_url
        self.description = description

        self._text = None

    @property
    def id(self):
        return f'{self.entry.id}__{self.name}'

    @property
    def name(self):
        return self.entry.docket.manager.document_get_name(
            self.entry.entry_number, self.attachment_number
        )

    @property
    def pdf_path(self):
        return self.entry.docket.manager.document_get_pdf_path(
            self.entry.entry_number, self.attachment_number
        )

    @property
    def ocr_path(self):
        return self.entry.docket.manager.document_get_ocr_path(
            self.entry.entry_number, self.attachment_number
        )

    @property
    def pdf_available(self):
        return self.pdf_path.exists()

    @property
    def ocr_needed(self):
        return not self.ocr_path.exists()

    @property
    def is_attachment(self):
        return self.attachment_number is not None

    @property
    def text(self):
        if self._text is None:
            if self.ocr_path.exists():
                self._text = json.loads(self.ocr_path.read_text())['content']
            else:
                self._text = ''
        return self._text

    def to_dict(self):
        return {
            'attachment_number': self.attachment_number,
            'pacer_url': self.pacer_url,
            'description': self.description,
            'pdf_available': self.pdf_available,
        }

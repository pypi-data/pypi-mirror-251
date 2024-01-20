

class DocumentMixin:
    def document_get_name(self, entry_number, attachment_number=None):
        return f'{entry_number}_{attachment_number or 0}'

    def document_get_pdf_path(self, entry_number, attachment_number=None):
        name = self.document_get_name(entry_number, attachment_number)
        return self.dir / f'doc.pdf.{name}.pdf'

    def document_get_ocr_path(self, entry_number, attachment_number=None):
        name = self.document_get_name(entry_number, attachment_number)
        return self.dir / f'doc.ocr.{name}.json'

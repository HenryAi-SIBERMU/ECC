from pypdf import PdfReader
reader = PdfReader('refrensi/Ref/OUTLINE STUDI D3TLH WITH COMMENT.pdf')
for i, page in enumerate(reader.pages):
    print(f"--- Page {i+1} ---")
    print(page.extract_text())
    if '/Annots' in page:
        for annot in page['/Annots']:
            obj = annot.get_object()
            if '/Contents' in obj:
                print("COMMENT:", obj['/Contents'])

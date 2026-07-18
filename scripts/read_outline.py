import docx
doc_path = r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\refrensi\Ref\OUTLINE STUDI D3TLH.docx'
try:
    doc = docx.Document(doc_path)
    for p in doc.paragraphs:
        if p.text.strip():
            print(p.text)
except Exception as e:
    print("Error:", e)

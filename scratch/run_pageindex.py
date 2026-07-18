import os
import sys
import time
from dotenv import load_dotenv
from pageindex.client import PageIndexClient

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY tidak ditemukan")
    sys.exit(1)

def run_pageindex(pdf_path, query):
    print(f"File: {pdf_path}")
    print(f"Prompt: {query}\n")
    
    try:
        client = PageIndexClient(api_key=api_key)
        
        # 1. Submit dokumen
        print("1. Mengunggah dokumen ke PageIndex...")
        doc_response = client.submit_document(file_path=pdf_path)
        doc_id = doc_response.get("document_id")
        
        if not doc_id:
            print("Gagal mendapatkan document_id")
            print(doc_response)
            return

        print(f"Document ID: {doc_id}")
        
        # 2. Tunggu indexing selesai (optional, tapi aman)
        print("2. Menunggu proses indexing...")
        time.sleep(15) 
        
        # 3. Chat completion (reasoning)
        print("3. Menjalankan query (Tree Search & Reasoning)...")
        messages = [
            {"role": "user", "content": query}
        ]
        
        response = client.chat_completions(
            document_id=doc_id,
            messages=messages,
            model="gpt-4o"
        )
        
        print("\n--- HASIL PAGEINDEX ---\n")
        print(response)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_pageindex(sys.argv[1], sys.argv[2])

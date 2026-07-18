import sys
from pathlib import Path

# Add project root to sys.path so we can import tools
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools.google_dork.google_dorker import google_dork

queries = [
    '"Global Tailings Portal" Indonesia nickel',
    '"RKL-RPL" OR "AMDAL" AND "tailing" OR "slag" "Indonesia" filetype:pdf'
]

for q in queries:
    print(f"\n{'='*50}\nTesting Query: {q}\n{'='*50}")
    google_dork(q, 3)

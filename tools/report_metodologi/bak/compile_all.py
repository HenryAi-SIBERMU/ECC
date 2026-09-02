#!/usr/bin/env python3
"""
Master Runner & Compiler Laporan Metodologi (CELIOS ECC)
Menjalankan seluruh generator bab metodologi dan menyimpannya di tools/report_metodologi/.
"""

import sys
import os
from pathlib import Path

def main():
    tool_dir = Path(__file__).resolve().parent

    target = sys.argv[1].lower() if len(sys.argv) > 1 else "bab1"

    if target in ["bab1", "all"]:
        print("\n>>> MENJALANKAN GENERATOR BAB 1 <<<")
        from generate_bab1 import generate_all_bab1
        generate_all_bab1()

if __name__ == "__main__":
    main()

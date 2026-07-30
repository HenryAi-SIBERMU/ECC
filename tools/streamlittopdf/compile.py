import pypandoc
import os
from pathlib import Path

CHAPTERS = [
    ("chapter_1.md", "v2_30072026_Laporan_Bab1"),
    ("chapter_2.md", "v2_30072026_Laporan_Bab2"),
    ("chapter_3.md", "v2_30072026_Laporan_Bab3"),
    ("chapter_4.md", "v2_30072026_Laporan_Bab4"),
    ("chapter_5.md", "v2_30072026_Laporan_Bab5"),
    ("chapter_6.md", "v2_30072026_Laporan_Bab6"),
    ("chapter_7.md", "v2_30072026_Laporan_Bab7"),
    ("chapter_8.md", "v2_30072026_Laporan_Bab8"),
    ("chapter_9.md", "v2_30072026_Laporan_Bab9"),
]

def compile_chapter(md_file: Path, out_stem: str, docs_dir: Path):
    if not md_file.exists():
        print(f"  SKIP: {md_file.name} not found")
        return

    docx_out = docs_dir / f"{out_stem}.docx"
    tex_out  = docs_dir / f"{out_stem}.tex"

    print(f"Compiling {md_file.name} to DOCX...")
    pypandoc.convert_file(
        str(md_file), 'docx', outputfile=str(docx_out),
        extra_args=['--resource-path', str(md_file.parent)]
    )
    print(f"Saved: {docx_out}")

    print(f"Compiling {md_file.name} to LaTeX...")
    pypandoc.convert_file(
        str(md_file), 'latex', outputfile=str(tex_out),
        extra_args=['--standalone', '--resource-path', str(md_file.parent)]
    )
    print(f"Saved: {tex_out}")

def main():
    base_dir = Path(__file__).resolve().parent.parent.parent
    here     = Path(__file__).resolve().parent
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    try:
        pypandoc.get_pandoc_version()
    except OSError:
        print("Pandoc not found. Downloading...")
        pypandoc.download_pandoc()

    import sys
    # Allow: python compile.py [bab1|bab2|all]
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    for md_name, stem in CHAPTERS:
        bab_key = stem.lower().replace("laporan_", "")  # e.g. "bab1"
        if target != "all" and target != bab_key:
            continue
        compile_chapter(here / md_name, stem, docs_dir)

    print("\nSUCCESS! Report compilation complete.")

if __name__ == "__main__":
    main()

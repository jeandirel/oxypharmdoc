import sys
from pathlib import Path
import pdfplumber


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from a single PDF file using pdfplumber."""
    text_parts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)


def process_pdfs(input_dir: Path, output_dir: Path) -> None:
    """Walk through input_dir and write PDF text to mirrored files in output_dir."""
    for pdf_file in input_dir.rglob("*.pdf"):
        relative_path = pdf_file.relative_to(input_dir)
        txt_file = output_dir / relative_path.with_suffix(".txt")
        txt_file.parent.mkdir(parents=True, exist_ok=True)
        text = extract_pdf_text(pdf_file)
        txt_file.write_text(text, encoding="utf-8")


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python extract_text.py <input_dir> <output_dir>")
        return 1
    input_dir = Path(argv[0])
    output_dir = Path(argv[1])
    process_pdfs(input_dir, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

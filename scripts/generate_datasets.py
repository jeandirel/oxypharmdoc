import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path


def extract_sections(text: str):
    """Split text into sections separated by blank lines."""
    sections = re.split(r"\n\s*\n", text)
    return [s.strip() for s in sections if s.strip()]


def summarize_section(section: str, max_sentences: int = 2) -> str:
    """Return summary of the section using the first few sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", section)
    summary = " ".join(sentences[:max_sentences]).strip()
    return summary


def generate_candidate_qa(text: str):
    pairs = []
    for section in extract_sections(text):
        summary = summarize_section(section)
        if not summary:
            continue
        question = summary.split(".")[0].strip()
        if not question.endswith("?"):
            question = f"{question}?"
        pairs.append({"question": question, "answer": summary})
    return pairs


def compute_keywords(mod_texts, top_k: int = 5):
    tokenized = {m: re.findall(r"\b\w+\b", t.lower()) for m, t in mod_texts.items()}
    term_freq = {m: Counter(tokens) for m, tokens in tokenized.items()}
    doc_freq = Counter()
    for tokens in tokenized.values():
        doc_freq.update(set(tokens))
    N = len(mod_texts)
    keywords = {}
    for module, counts in term_freq.items():
        total = sum(counts.values()) or 1
        scores = {}
        for token, count in counts.items():
            tf = count / total
            idf = math.log((N + 1) / (doc_freq[token] + 1)) + 1
            scores[token] = tf * idf
        top = sorted(scores, key=scores.get, reverse=True)[:top_k]
        keywords[module] = top
    return keywords


def process_directory(input_dir: Path):
    syllabus = {}
    mod_texts = {}
    for path in sorted(Path(input_dir).glob("*.txt")):
        module = path.stem
        text = path.read_text(encoding="utf-8")
        mod_texts[module] = text
        syllabus[module] = generate_candidate_qa(text)
    keywords = compute_keywords(mod_texts)
    return syllabus, keywords


def save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate syllabus and keyword datasets")
    parser.add_argument("input_dir", help="Directory containing extracted text files")
    parser.add_argument("output_dir", help="Directory where JSON files will be saved")
    args = parser.parse_args()

    syllabus, keywords = process_directory(Path(args.input_dir))
    out_dir = Path(args.output_dir)
    save_json(syllabus, out_dir / "syllabus_qr.json")
    save_json(keywords, out_dir / "keywords_doc.json")


if __name__ == "__main__":
    main()

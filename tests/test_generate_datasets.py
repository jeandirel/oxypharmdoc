import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts import generate_datasets


def test_syllabus_and_keywords(tmp_path):
    text_dir = tmp_path / "texts"
    text_dir.mkdir()
    (text_dir / "module1.txt").write_text("First section. More text.\n\nSecond part with extra.")
    (text_dir / "module2.txt").write_text("Another module text example.")
    out_dir = tmp_path / "out"

    syllabus, keywords = generate_datasets.process_directory(text_dir)
    generate_datasets.save_json(syllabus, out_dir / "syllabus_qr.json")
    generate_datasets.save_json(keywords, out_dir / "keywords_doc.json")

    syllabus_data = json.loads((out_dir / "syllabus_qr.json").read_text())
    keywords_data = json.loads((out_dir / "keywords_doc.json").read_text())

    assert isinstance(syllabus_data, dict)
    assert set(syllabus_data.keys()) == {"module1", "module2"}
    assert isinstance(syllabus_data["module1"], list)
    assert "question" in syllabus_data["module1"][0]
    assert "answer" in syllabus_data["module1"][0]

    assert isinstance(keywords_data, dict)
    assert set(keywords_data.keys()) == {"module1", "module2"}
    assert isinstance(keywords_data["module1"], list)
    assert all(isinstance(k, str) for k in keywords_data["module1"])

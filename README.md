# Oxypharm Documentation Dataset

This repository contains PDF and presentation files used to build an internal knowledge base for Oxypharm. The scripts referenced below are expected to be available in your environment and are used to convert these source files into text and dataset files compatible with a Retrieval-Augmented Generation (RAG) chatbot.

## Requirements

- Python 3.10+
- Recommended dependencies:
  - `pdfminer.six` (for PDF text extraction)
  - `pandas` (for dataset creation)
  - `tqdm` (optional progress bars)

Install the dependencies with pip:

```bash
pip install pdfminer.six pandas tqdm
```

## Usage

1. **Extract text from documents**

   ```bash
   python extract_text.py <input_dir> <output_dir>
   ```

   - `<input_dir>`: directory containing the PDF and PPTX files.
   - `<output_dir>`: location where the extracted `.txt` files will be saved.

2. **Generate dataset for the chatbot**

   ```bash
   python generate_datasets.py <text_dir> <dataset_dir>
   ```

   - `<text_dir>`: directory of `.txt` files produced by `extract_text.py`.
   - `<dataset_dir>`: target directory for the dataset (CSV or JSON) used by the RAG system.

The resulting dataset can then be indexed or uploaded to the chatbot project's vector store, allowing the assistant to retrieve relevant context from these documents at runtime.

## Testing

Run unit tests with [`pytest`](https://docs.pytest.org/) if any tests are provided:

```bash
pytest
```

`pytest` will report `no tests ran` if there are currently no test files.


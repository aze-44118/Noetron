# Database Directory

This directory contains processed CSV files with vectorized sentences.

## Sample Files

- `spinoza_en_sample.csv` - Sample vectorized sentences from Spinoza (English)
- `spinoza_fr_sample.csv` - Sample vectorized sentences from Spinoza (French)

## File Format

Each CSV file contains the following columns:

- `sentence_id`: Unique identifier for each sentence
- `text`: The actual sentence text
- `source`: Source file name
- `vector`: JSON-serialized embedding vector (1024 dimensions)

## Usage

These sample files can be used for testing Noetron's search and comparison features:

```bash
# Search in English sample
python cli/main.py search -p "freedom and necessity" -f database/spinoza_en_sample.csv

# Compare samples
python cli/main.py compare -s database/spinoza_en_sample.csv -d database/spinoza_fr_sample.csv
```

## Note

The full database files are excluded from version control due to their size. Only sample files are included for demonstration purposes.

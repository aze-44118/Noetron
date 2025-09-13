# Noetron v1.0

🔮 **Noetron** is a powerful semantic analysis tool designed for processing and analyzing textual corpora using state-of-the-art sentence transformers and cosine similarity.

## Features

- **Sentence Extraction**: Intelligent extraction of sentences from text files with advanced filtering
- **Semantic Vectorization**: Uses BAAI/bge-m3 model for high-quality multilingual embeddings
- **Semantic Search**: Find semantically similar sentences using cosine similarity
- **Corpus Comparison**: Compare different corpora to find cross-document similarities
- **Interactive Mode**: Command-line interface with interactive environment
- **Multi-language Support**: Works with multiple languages including French and English

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/noetron.git
   cd noetron
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Extract Sentences

Extract sentences from text files in a directory:

```bash
python cli/main.py extractor -i data_folder --csv
```

### 2. Process Complete Pipeline

Extract, vectorize, and process text files:

```bash
python cli/main.py process -i data_folder
```

### 3. Semantic Search

Search for semantically similar sentences:

```bash
python cli/main.py search -p "your search query" -f database/processed_file.csv --top 5
```

### 4. Compare Corpora

Compare two different corpora:

```bash
python cli/main.py compare -s database/source.csv -d database/destination.csv --top 10
```

### 5. Interactive Mode

Launch the interactive environment:

```bash
./noetron activate database/processed_file.csv
```

## Usage Examples

### Basic Workflow

```bash
# 1. Process a folder of text files
python cli/main.py process -i philosophical_texts

# 2. Search for similar concepts
python cli/main.py search -p "freedom and existence" -f database/philosophical_texts.csv --top 3

# 3. Compare different authors
python cli/main.py compare -s database/spinoza.csv -d database/merleau_ponty.csv --top 5
```

### Interactive Commands

Once in interactive mode (`./noetron activate database/file.csv`):

```bash
# Search for concepts
search "philosophy of perception" --top 5

# Compare corpora
compare database/source.csv database/dest.csv --top 3 --length 50

# Get help
help
```

## Command Reference

### Extractor Command

```bash
python cli/main.py extractor -i <folder> [options]
```

**Options:**
- `-i, --input`: Input folder (required)
- `--csv`: Create CSV output
- `--debug`: Enable debug mode
- `--start`: Starting phrase for filtering
- `--interactive`: Interactive mode for each file

### Process Command

```bash
python cli/main.py process -i <folder> [options]
```

**Options:**
- `-i, --input`: Input folder (required)
- `--debug`: Enable debug mode

### Search Command

```bash
python cli/main.py search -p <phrase> -f <csv_file> [options]
```

**Options:**
- `-p, --phrase`: Search phrase (required)
- `-f, --file`: CSV file path (required)
- `--top`: Number of results (default: 3)
- `--debug`: Enable debug mode

### Compare Command

```bash
python cli/main.py compare -s <source_csv> -d <dest_csv> [options]
```

**Options:**
- `-s, --source`: Source CSV file (required)
- `-d, --destination`: Destination CSV file (required)
- `-t, --top`: Number of results (default: 3)
- `-l, --length`: Minimum sentence length (default: 0)
- `--debug`: Enable debug mode

## Project Structure

```
noetron/
├── cli/                    # Command-line interface
│   ├── main.py            # Main CLI entry point
│   ├── extractor.py       # Sentence extraction
│   ├── process.py         # Complete processing pipeline
│   ├── search.py          # Semantic search
│   ├── compare.py         # Corpus comparison
│   └── vectorize.py       # Text vectorization
├── processing/             # Text processing modules
│   └── txt_processer.py   # Sentence extraction logic
├── data/                   # Input text files
├── database/               # Processed CSV files
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Technical Details

### Sentence Extraction

Noetron uses sophisticated rules for sentence extraction:

- **Start**: Capital letter at beginning of line or after period
- **End**: Period followed by capital letter or line break
- **Filtering**: Removes notes, references, and formatting artifacts
- **Abbreviation Detection**: Handles common abbreviations correctly

### Vectorization

- **Model**: BAAI/bge-m3 (multilingual, high-performance)
- **Dimensions**: 1024-dimensional embeddings
- **Format**: JSON-serialized vectors in CSV files

### Similarity Calculation

- **Method**: Cosine similarity between normalized vectors
- **Range**: 0 to 1 (higher = more similar)
- **Performance**: Optimized for large corpora

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

The project follows PEP 8 guidelines. Use a formatter like `black`:

```bash
pip install black
black .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) for the excellent multilingual embedding model
- [sentence-transformers](https://www.sbert.net/) for the powerful sentence embedding framework
- The open-source community for inspiration and tools

## Changelog

### v1.0.0
- Initial release
- Sentence extraction with advanced filtering
- Semantic search and corpus comparison
- Interactive command-line interface
- Multi-language support
- Professional documentation

---

**Noetron** - Unlock the semantic structure of your texts 🔮
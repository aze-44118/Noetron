# Tests Directory

This directory contains unit tests for Noetron.

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_extractor.py
```

## Test Structure

- `test_extractor.py` - Tests for sentence extraction
- `test_vectorize.py` - Tests for text vectorization
- `test_search.py` - Tests for semantic search
- `test_compare.py` - Tests for corpus comparison

## Adding Tests

When adding new features, please include corresponding tests to ensure code quality and reliability.

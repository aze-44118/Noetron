#!/usr/bin/env python3
"""
Sentence vectorization module for Noetron
"""

import csv
import json
import numpy as np
from pathlib import Path
from typing import Union, List, Dict
from sentence_transformers import SentenceTransformer


def vectorize_sentences(csv_path: Union[str, Path], debug: bool = False) -> None:
    """
    Vectorize sentences from a CSV file using BAAI/bge-m3
    Args:
        csv_path: Path to the CSV file containing sentences
        debug: Debug mode to display more information
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"Error: File '{csv_path}' does not exist.")
        return
    
    print("=== SENTENCE VECTORIZATION ===")
    
    # Load the BAAI/bge-m3 model
    if debug:
        print("  Loading BAAI/bge-m3 model...")
    
    try:
        model = SentenceTransformer('BAAI/bge-m3')
        if debug:
            print("  Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Read the CSV
    sentences_data = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sentences_data.append(row)
    
    if debug:
        print(f"  {len(sentences_data)} sentences to vectorize")
    
    # Extract sentence texts
    texts = [row['text'] for row in sentences_data]
    
    # Vectorize the sentences
    if debug:
        print("  Vectorization in progress...")
    
    try:
        embeddings = model.encode(texts, show_progress_bar=debug)
        if debug:
            print(f"  Vectorization completed. Dimensions: {embeddings.shape}")
    except Exception as e:
        print(f"Error during vectorization: {e}")
        return
    
    # Add vectors to data
    for i, row in enumerate(sentences_data):
        # Convert vector to list for JSON
        vector_list = embeddings[i].tolist()
        row['vector'] = json.dumps(vector_list)
    
    # Write the updated CSV
    output_path = csv_path.parent / f"{csv_path.stem}_vectorized.csv"
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['sentence_id', 'text', 'source', 'vector']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sentences_data)
        
        print(f"=== RESULT ===")
        print(f"Vectorized CSV created: {output_path}")
        print(f"Number of vectorized sentences: {len(sentences_data)}")
        print(f"Vector dimensions: {embeddings.shape[1]}")
        
    except Exception as e:
        print(f"Error writing CSV: {e}")


def vectorize_sentences_from_list(sentences: List[Dict], debug: bool = False) -> List[Dict]:
    """
    Vectorize a list of sentences and return data with vectors
    Args:
        sentences: List of dictionaries containing sentences
        debug: Debug mode to display more information
    Returns:
        List of dictionaries with added vectors
    """
    if not sentences:
        print("No sentences to vectorize")
        return sentences
    
    print("=== SENTENCE VECTORIZATION ===")
    
    # Load the BAAI/bge-m3 model
    if debug:
        print("  Loading BAAI/bge-m3 model...")
    
    try:
        model = SentenceTransformer('BAAI/bge-m3')
        if debug:
            print("  Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return sentences
    
    # Extract sentence texts
    texts = [sentence['text'] for sentence in sentences]
    
    # Vectorize the sentences
    if debug:
        print(f"  Vectorizing {len(texts)} sentences...")
    
    try:
        embeddings = model.encode(texts, show_progress_bar=debug)
        if debug:
            print(f"  Vectorization completed. Dimensions: {embeddings.shape}")
    except Exception as e:
        print(f"Error during vectorization: {e}")
        return sentences
    
    # Add vectors to data
    for i, sentence in enumerate(sentences):
        # Convert vector to list for JSON
        vector_list = embeddings[i].tolist()
        sentence['vector'] = json.dumps(vector_list)
    
    if debug:
        print(f"  {len(sentences)} sentences vectorized successfully")
    
    return sentences


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        vectorize_sentences(sys.argv[1], debug=True)
    else:
        print("Usage: python vectorize.py <csv_path>")

#!/usr/bin/env python3
"""
Corpus comparison module for Noetron
"""

import csv
import json
import numpy as np
from pathlib import Path
from typing import Union, List, Dict, Tuple
from sentence_transformers import SentenceTransformer


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors
    Args:
        vec1: First vector
        vec2: Second vector
    Returns:
        Similarity score between 0 and 1
    """
    # Normalize vectors
    vec1_norm = vec1 / np.linalg.norm(vec1)
    vec2_norm = vec2 / np.linalg.norm(vec2)
    
    # Calculate cosine similarity
    similarity = np.dot(vec1_norm, vec2_norm)
    return float(similarity)


def load_vectorized_sentences(csv_path: Union[str, Path]) -> List[Dict]:
    """
    Load vectorized sentences from a CSV file
    Args:
        csv_path: Path to the vectorized CSV file
    Returns:
        List of sentences with their vectors
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"File '{csv_path}' does not exist.")
    
    sentences = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert JSON vector to numpy array
            if row['vector']:
                vector = np.array(json.loads(row['vector']))
                sentences.append({
                    'sentence_id': int(row['sentence_id']),
                    'text': row['text'],
                    'source': row['source'],
                    'vector': vector
                })
    
    return sentences


def compare_corpus(
    source_csv: Union[str, Path],
    destination_csv: Union[str, Path],
    top_k: int = 3,
    min_length: int = 0,
    debug: bool = False
) -> List[Dict]:
    """
    Compare two corpora and find the most similar sentences
    Args:
        source_csv: Path to the source CSV file
        destination_csv: Path to the destination CSV file
        top_k: Total number of results to return
        min_length: Minimum length of sentences to compare (in characters)
        debug: Debug mode to display more information
    Returns:
        List of top_k comparisons with similarity scores
    """
    if debug:
        print(f"=== CORPUS COMPARISON ===")
        print(f"Source: {source_csv}")
        print(f"Destination: {destination_csv}")
        print(f"Global Top K: {top_k}")
        if min_length > 0:
            print(f"Minimum sentence length: {min_length} characters")
    
    # Load vectorized sentences
    if debug:
        print("  Loading source sentences...")
    
    try:
        source_sentences = load_vectorized_sentences(source_csv)
        if debug:
            print(f"  {len(source_sentences)} source sentences loaded")
    except Exception as e:
        print(f"Error loading source sentences: {e}")
        return []
    
    if debug:
        print("  Loading destination sentences...")
    
    try:
        dest_sentences = load_vectorized_sentences(destination_csv)
        if debug:
            print(f"  {len(dest_sentences)} destination sentences loaded")
    except Exception as e:
        print(f"Error loading destination sentences: {e}")
        return []
    
    # Filter by length if specified
    if min_length > 0:
        if debug:
            print(f"  Filtering sentences by minimum length ({min_length} characters)...")
        
        original_source_count = len(source_sentences)
        original_dest_count = len(dest_sentences)
        
        source_sentences = [s for s in source_sentences if len(s['text']) >= min_length]
        dest_sentences = [s for s in dest_sentences if len(s['text']) >= min_length]
        
        if debug:
            print(f"  Source sentences after filtering: {len(source_sentences)}/{original_source_count}")
            print(f"  Destination sentences after filtering: {len(dest_sentences)}/{original_dest_count}")
    
    # Compare each source sentence with all destination sentences
    if debug:
        print("  Calculating similarities between corpora...")
    
    all_similarities = []
    
    for source_sent in source_sentences:
        for dest_sent in dest_sentences:
            similarity = cosine_similarity(source_sent['vector'], dest_sent['vector'])
            all_similarities.append({
                'source_sentence_id': source_sent['sentence_id'],
                'source_text': source_sent['text'],
                'source_source': source_sent['source'],
                'dest_sentence_id': dest_sent['sentence_id'],
                'dest_text': dest_sent['text'],
                'dest_source': dest_sent['source'],
                'similarity_score': similarity
            })
    
    # Sort all similarities by score (descending)
    all_similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    # Take the global top_k
    top_similarities = all_similarities[:top_k]
    
    # Add global rank
    for i, sim in enumerate(top_similarities):
        sim['rank'] = i + 1
    
    if debug:
        print(f"  Comparison completed. Top {len(top_similarities)} results found.")
    
    return top_similarities


def compare_corpus_cli(
    source_csv: Union[str, Path],
    destination_csv: Union[str, Path],
    top_k: int = 3,
    min_length: int = 0,
    debug: bool = False
) -> None:
    """
    CLI interface for corpus comparison
    Args:
        source_csv: Path to the source CSV file
        destination_csv: Path to the destination CSV file
        top_k: Total number of results to display
        min_length: Minimum length of sentences to compare (in characters)
        debug: Debug mode
    """
    try:
        results = compare_corpus(source_csv, destination_csv, top_k, min_length, debug)
        
        if not results:
            print("No results found.")
            return
        
        print(f"\n=== COMPARISON RESULTS ===")
        print(f"Source: {source_csv}")
        print(f"Destination: {destination_csv}")
        print(f"Global Top K: {top_k}")
        if min_length > 0:
            print(f"Minimum sentence length: {min_length} characters")
        print(f"Total number of results: {len(results)}")
        print()
        
        # Display results by global rank
        for result in results:
            print(f"🏆 RANK {result['rank']} (Score: {result['similarity_score']:.4f})")
            print(f"📖 SOURCE SENTENCE {result['source_sentence_id']}:")
            print(f"   {result['source_text'][:150]}{'...' if len(result['source_text']) > 150 else ''}")
            print(f"   📁 Source: {result['source_source']}")
            print(f"📖 DESTINATION SENTENCE {result['dest_sentence_id']}:")
            print(f"   {result['dest_text'][:150]}{'...' if len(result['dest_text']) > 150 else ''}")
            print(f"   📁 Source: {result['dest_source']}")
            print("-" * 80)
        
    except Exception as e:
        print(f"Error during comparison: {e}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Compare two corpora using cosine similarity"
    )
    
    parser.add_argument(
        'source_csv',
        help='Path to the source CSV file'
    )
    
    parser.add_argument(
        'destination_csv',
        help='Path to the destination CSV file'
    )
    
    parser.add_argument(
        '--top', '-t',
        type=int,
        default=3,
        help='Number of results to display per sentence (default: 3)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode to display more information'
    )
    
    args = parser.parse_args()
    
    compare_corpus_cli(args.source_csv, args.destination_csv, args.top, args.debug)

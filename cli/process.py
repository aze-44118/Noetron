#!/usr/bin/env python3
"""
Complete data processing module for Noetron
"""

import csv
from pathlib import Path
from typing import Union
from cli.extractor import extract_sentences
from cli.vectorize import vectorize_sentences_from_list


def process_data(input_path: Union[str, Path], debug: bool = False) -> None:
    """
    Process a folder of TXT files: extraction + vectorization + other treatments
    Args:
        input_path: Path to the folder containing TXT files
        debug: Debug mode to display more information
    """
    input_path = Path(input_path)
    database_dir = Path(__file__).parent.parent / 'database'
    database_dir.mkdir(exist_ok=True)
    
    if not input_path.exists():
        print(f"Error: Folder '{input_path}' does not exist.")
        return
    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a folder.")
        return
    
    print("=== STEP 1: Sentence extraction ===")
    # Use the extraction function
    all_sentences = extract_sentences(input_path, create_csv=False, debug=debug)
    
    if not all_sentences:
        print("No sentences extracted. Stopping processing.")
        return
    
    print(f"=== STEP 2: Sentence vectorization ===")
    # Vectorize the sentences
    all_sentences = vectorize_sentences_from_list(all_sentences, debug=debug)
    
    print("=== STEP 3: Other treatments ===")
    # TODO: Add other treatments here
    if debug:
        print("  Other treatments in progress...")
    
    # Write the final CSV
    output_filename = f"{input_path.name}.csv"
    output_path = database_dir / output_filename
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['sentence_id', 'text', 'source', 'vector'])
            for sentence_data in all_sentences:
                writer.writerow([
                    sentence_data['sentence_id'],
                    sentence_data['text'],
                    sentence_data['source'],
                    sentence_data['vector']
                ])
        print(f"=== RESULT ===")
        print(f"CSV created: {output_path}")
        print(f"Number of processed sentences: {len(all_sentences)}")
    except Exception as e:
        print(f"Error writing CSV: {e}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        process_data(sys.argv[1])
    else:
        print("Usage: python process.py <folder_path>")

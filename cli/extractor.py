#!/usr/bin/env python3
"""
Sentence extraction module for Noetron
"""

import csv
from pathlib import Path
from typing import Union
from processing.txt_processer import SentenceExtractor


def extract_sentences(input_path: Union[str, Path], create_csv: bool = False, debug: bool = False, start_phrase: str = None, interactive: bool = False) -> None:
    """
    Extract sentences from a folder of TXT files
    Args:
        input_path: Path to the folder containing TXT files
        create_csv: If True, creates a CSV file with extracted sentences
        debug: Debug mode to display more information
        start_phrase: Starting phrase to filter content (optional, used if interactive=False)
        interactive: If True, prompts for starting phrase for each file
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Error: Folder '{input_path}' does not exist.")
        return
    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a folder.")
        return
    
    txt_files = list(input_path.glob("*.txt"))
    if not txt_files:
        print(f"No TXT files found in '{input_path}'")
        return
    
    print(f"Extracting sentences from {len(txt_files)} TXT file(s)...")
    
    all_sentences = []
    sentence_id = 1
    
    for txt_file in txt_files:
        if debug:
            print(f"\nProcessing file: {txt_file.name}")
        else:
            print(f"\n📁 Processing: {txt_file.name}")
        
        # Ask for starting phrase for this file if interactive mode
        current_start_phrase = start_phrase
        if interactive:
            current_start_phrase = input(f"What is the sentence for {txt_file.name}? ")
            if current_start_phrase.strip():
                print(f"🎯 Filtering from: '{current_start_phrase}'")
            else:
                print("ℹ️  No starting phrase specified, processing complete file")
                current_start_phrase = None
        
        extractor = SentenceExtractor(txt_file)
        sentences = extractor.extract_sentences(start_phrase=current_start_phrase)
        
        if debug:
            print(f"  Number of sentences extracted: {len(sentences)}")
            if sentences:
                print(f"  First sentence: {sentences[0][:100]}...")
                print(f"  Last sentence: {sentences[-1][:100]}...")
        else:
            print(f"  ✅ {len(sentences)} sentences extracted")
        
        # Add metadata for each sentence
        for sentence in sentences:
            all_sentences.append({
                'sentence_id': sentence_id,
                'text': sentence,
                'source': txt_file.name,
                'vector': ''  # Empty for extraction only
            })
            sentence_id += 1
    
    print(f"\n🎉 Total sentences extracted: {len(all_sentences)}")
    
    # Create CSV if requested
    if create_csv:
        database_dir = Path(__file__).parent.parent / 'database'
        database_dir.mkdir(exist_ok=True)
        
        output_filename = f"{input_path.name}_sentences.csv"
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
            print(f"💾 CSV created: {output_path}")
        except Exception as e:
            print(f"❌ Error writing CSV: {e}")
    
    return all_sentences


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        extract_sentences(sys.argv[1], create_csv=True)
    else:
        print("Usage: python extractor.py <folder_path> [--csv]") 
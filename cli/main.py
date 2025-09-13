#!/usr/bin/env python3
"""
Noetron CLI Entry Point
Command-line interface for Noetron semantic analysis tool
"""

import argparse
import os
import sys
from pathlib import Path

# Add the parent directory to the path for module imports
sys.path.append(str(Path(__file__).parent.parent))

from cli.process import process_data
from cli.extractor import extract_sentences
from cli.search import search_sentences_cli
from cli.compare import compare_corpus_cli


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Noetron - Data processing and analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python main.py extractor -i my_folder
  python main.py extractor -i /path/to/folder --csv
  python main.py extractor -i my_folder --interactive
  python main.py extractor -i my_folder --interactive --csv
  python main.py process -i my_folder
  python main.py process -i /path/to/folder
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # Extractor command
    extractor_parser = subparsers.add_parser(
        'extractor',
        help='Extract sentences from data files (interactive mode available with --interactive)'
    )
    
    extractor_parser.add_argument(
        '-i', '--input',
        required=True,
        help='Folder name to process (located in data folder) or full path to a folder'
    )
    
    extractor_parser.add_argument(
        '--csv',
        action='store_true',
        help='Create a CSV file with extracted sentences'
    )
    
    extractor_parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode to display more information'
    )
    
    extractor_parser.add_argument(
        '--start',
        type=str,
        help='Starting phrase to filter content (e.g., "Maurice MERLEAU-PONTY SIGNES")'
    )
    
    extractor_parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode: prompts for starting phrase for each TXT file'
    )
    
    # Process command
    process_parser = subparsers.add_parser(
        'process',
        help='Process data files (extraction + vectorization + other treatments)'
    )
    
    process_parser.add_argument(
        '-i', '--input',
        required=True,
        help='Folder name to process (located in data folder) or full path to a folder'
    )
    
    process_parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode to display more information'
    )
    
    # Search command
    search_parser = subparsers.add_parser(
        'search',
        help='Search for similar sentences using cosine similarity'
    )
    
    search_parser.add_argument(
        '-p', '--phrase',
        required=True,
        help='Search phrase'
    )
    
    search_parser.add_argument(
        '-f', '--file',
        required=True,
        help='Path to the vectorized CSV file'
    )
    
    search_parser.add_argument(
        '--top',
        type=int,
        default=3,
        help='Number of results to display (default: 3)'
    )
    
    search_parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode to display more information'
    )
    
    # Compare command
    compare_parser = subparsers.add_parser(
        'compare',
        help='Compare two corpora and find the most similar sentences'
    )
    
    compare_parser.add_argument(
        '-s', '--source',
        required=True,
        help='Path to the source CSV file'
    )
    
    compare_parser.add_argument(
        '-d', '--destination',
        required=True,
        help='Path to the destination CSV file'
    )
    
    compare_parser.add_argument(
        '-t', '--top',
        type=int,
        default=3,
        help='Total number of results to display (default: 3)'
    )
    
    compare_parser.add_argument(
        '-l', '--length',
        type=int,
        default=0,
        help='Minimum length of sentences to compare in characters (default: 0 = no limit)'
    )
    
    compare_parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode to display more information'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'search':
        print(f"Semantic search for: '{args.phrase}'")
        search_sentences_cli(args.phrase, args.file, args.top, args.debug)
        return
    
    elif args.command == 'compare':
        print(f"Corpus comparison: {args.source} → {args.destination}")
        compare_corpus_cli(args.source, args.destination, args.top, args.length, args.debug)
        return
    
    # For extractor and process commands, check the input path
    if not hasattr(args, 'input'):
        print("Error: Missing 'input' argument.")
        sys.exit(1)
    
    # Check if the path is relative or absolute
    if os.path.isabs(args.input):
        # Absolute path provided
        input_path = Path(args.input)
    else:
        # Relative path - look in the data folder
        data_dir = Path(__file__).parent.parent / 'data'
        input_path = data_dir / args.input
    
    # Check if the folder exists
    if not input_path.exists():
        print(f"Error: Folder '{input_path}' does not exist.")
        sys.exit(1)
    
    if args.command == 'extractor':
        print(f"Extracting sentences from folder: {input_path}")
        extract_sentences(input_path, create_csv=args.csv, debug=args.debug, start_phrase=args.start, interactive=args.interactive)
    
    elif args.command == 'process':
        print(f"Complete processing of folder: {input_path}")
        process_data(input_path, debug=args.debug)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Point d'entrée CLI pour Noetron
"""

import argparse
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from cli.process import process_data
from cli.extractor import extract_sentences
from cli.search import search_sentences_cli


def main():
    """Point d'entrée principal du CLI"""
    parser = argparse.ArgumentParser(
        description="Noetron - Outil de traitement et d'analyse de données",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py extractor -i mon_dossier
  python main.py extractor -i /chemin/vers/dossier --csv
  python main.py process -i mon_dossier
  python main.py process -i /chemin/vers/dossier
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Commandes disponibles'
    )
    
    # Commande extractor
    extractor_parser = subparsers.add_parser(
        'extractor',
        help='Extraire les phrases d\'un fichier de données'
    )
    
    extractor_parser.add_argument(
        '-i', '--input',
        required=True,
        help='Nom du dossier à traiter (situé dans le dossier data) ou chemin complet vers un dossier'
    )
    
    extractor_parser.add_argument(
        '--csv',
        action='store_true',
        help='Créer un fichier CSV avec les phrases extraites'
    )
    
    extractor_parser.add_argument(
        '--debug',
        action='store_true',
        help='Mode debug pour afficher plus d\'informations'
    )
    
    extractor_parser.add_argument(
        '--start',
        type=str,
        help='Phrase de départ pour filtrer le contenu (ex: "Maurice MERLEAU-PONTY SIGNES")'
    )
    
    # Commande process
    process_parser = subparsers.add_parser(
        'process',
        help='Traiter un fichier de données (extraction + vectorisation + autres traitements)'
    )
    
    process_parser.add_argument(
        '-i', '--input',
        required=True,
        help='Nom du dossier à traiter (situé dans le dossier data) ou chemin complet vers un dossier'
    )
    
    process_parser.add_argument(
        '--debug',
        action='store_true',
        help='Mode debug pour afficher plus d\'informations'
    )
    
    # Commande search
    search_parser = subparsers.add_parser(
        'search',
        help='Rechercher des phrases similaires avec similarité cosinus'
    )
    
    search_parser.add_argument(
        '-p', '--phrase',
        required=True,
        help='Phrase de recherche'
    )
    
    search_parser.add_argument(
        '-f', '--file',
        required=True,
        help='Chemin vers le fichier CSV vectorisé'
    )
    
    search_parser.add_argument(
        '--top',
        type=int,
        default=3,
        help='Nombre de résultats à afficher (défaut: 3)'
    )
    
    search_parser.add_argument(
        '--debug',
        action='store_true',
        help='Mode debug pour afficher plus d\'informations'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'search':
        print(f"Recherche sémantique pour: '{args.phrase}'")
        search_sentences_cli(args.phrase, args.file, args.top, args.debug)
        return
    
    # Pour les commandes extractor et process, vérifier le chemin d'entrée
    if not hasattr(args, 'input'):
        print("Erreur: Argument 'input' manquant.")
        sys.exit(1)
    
    # Vérifier si le chemin est relatif ou absolu
    if os.path.isabs(args.input):
        # Chemin absolu fourni
        input_path = Path(args.input)
    else:
        # Chemin relatif - chercher dans le dossier data
        data_dir = Path(__file__).parent.parent / 'data'
        input_path = data_dir / args.input
    
    # Vérifier que le dossier existe
    if not input_path.exists():
        print(f"Erreur: Le dossier '{input_path}' n'existe pas.")
        sys.exit(1)
    
    if args.command == 'extractor':
        print(f"Extraction des phrases du dossier: {input_path}")
        extract_sentences(input_path, create_csv=args.csv, debug=args.debug, start_phrase=args.start)
    
    elif args.command == 'process':
        print(f"Traitement complet du dossier: {input_path}")
        process_data(input_path, debug=args.debug)


if __name__ == '__main__':
    main()

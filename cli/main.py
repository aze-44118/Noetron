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


def main():
    """Point d'entrée principal du CLI"""
    parser = argparse.ArgumentParser(
        description="Noetron - Outil de traitement et d'analyse de données",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py process -i mon_dossier
  python main.py process -i /chemin/vers/dossier
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Commandes disponibles'
    )
    
    # Commande process
    process_parser = subparsers.add_parser(
        'process',
        help='Traiter un fichier de données'
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
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'process':
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
        
        print(f"Traitement du dossier: {input_path}")
        process_data(input_path, debug=args.debug)


if __name__ == '__main__':
    main()

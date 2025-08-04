#!/usr/bin/env python3
"""
Module de traitement complet des données pour Noetron
"""

import csv
from pathlib import Path
from typing import Union
from cli.extractor import extract_sentences
from cli.vectorize import vectorize_sentences_from_list


def process_data(input_path: Union[str, Path], debug: bool = False) -> None:
    """
    Traite un dossier de fichiers TXT : extraction + vectorisation + autres traitements
    Args:
        input_path: Chemin vers le dossier contenant les fichiers TXT
        debug: Mode debug pour afficher plus d'informations
    """
    input_path = Path(input_path)
    database_dir = Path(__file__).parent.parent / 'database'
    database_dir.mkdir(exist_ok=True)
    
    if not input_path.exists():
        print(f"Erreur: Le dossier '{input_path}' n'existe pas.")
        return
    if not input_path.is_dir():
        print(f"Erreur: '{input_path}' n'est pas un dossier.")
        return
    
    print("=== ÉTAPE 1: Extraction des phrases ===")
    # Utiliser la fonction d'extraction
    all_sentences = extract_sentences(input_path, create_csv=False, debug=debug)
    
    if not all_sentences:
        print("Aucune phrase extraite. Arrêt du traitement.")
        return
    
    print(f"=== ÉTAPE 2: Vectorisation des phrases ===")
    # Vectoriser les phrases
    all_sentences = vectorize_sentences_from_list(all_sentences, debug=debug)
    
    print("=== ÉTAPE 3: Autres traitements ===")
    # TODO: Ajouter d'autres traitements ici
    if debug:
        print("  Autres traitements en cours...")
    
    # Écriture du CSV final
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
        print(f"=== RÉSULTAT ===")
        print(f"CSV créé: {output_path}")
        print(f"Nombre de phrases traitées: {len(all_sentences)}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du CSV: {e}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        process_data(sys.argv[1])
    else:
        print("Usage: python process.py <chemin_vers_dossier>")

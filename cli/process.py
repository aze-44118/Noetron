#!/usr/bin/env python3
"""
Module de traitement des données pour Noetron
"""

import csv
from pathlib import Path
from typing import Union
from processing.txt_processer import ParagraphExtractor


def process_data(input_path: Union[str, Path]) -> None:
    """
    Traite un dossier de fichiers TXT et les convertit en CSV (paragraphe par ligne)
    Args:
        input_path: Chemin vers le dossier contenant les fichiers TXT
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
    
    output_filename = f"{input_path.name}.csv"
    output_path = database_dir / output_filename
    txt_files = list(input_path.glob("*.txt"))
    if not txt_files:
        print(f"Aucun fichier TXT trouvé dans '{input_path}'")
        return
    print(f"Traitement de {len(txt_files)} fichier(s) TXT...")
    
    all_paragraphs = []
    paragraph_id = 1
    
    for txt_file in txt_files:
        extractor = ParagraphExtractor(txt_file)
        paragraphs = extractor.extract_paragraphs()
        
        # Ajouter les métadonnées pour chaque paragraphe
        for para in paragraphs:
            all_paragraphs.append({
                'paragraph_id': paragraph_id,
                'text': para,
                'source': txt_file.name,
                'vector': ''  # Futur vecteur
            })
            paragraph_id += 1
    
    # Écriture du CSV
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['paragraph_id', 'text', 'source', 'vector'])
            for para_data in all_paragraphs:
                writer.writerow([
                    para_data['paragraph_id'],
                    para_data['text'],
                    para_data['source'],
                    para_data['vector']
                ])
        print(f"CSV créé: {output_path}")
        print(f"Nombre de paragraphes extraits: {len(all_paragraphs)}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du CSV: {e}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        process_data(sys.argv[1])
    else:
        print("Usage: python process.py <chemin_vers_dossier>")

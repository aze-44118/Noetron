#!/usr/bin/env python3
"""
Module de traitement des données pour Noetron
"""

import csv
from pathlib import Path
from typing import Union
from processing.txt_processer import SentenceExtractor


def process_data(input_path: Union[str, Path], debug: bool = False) -> None:
    """
    Traite un dossier de fichiers TXT et les convertit en CSV (phrase par ligne)
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
    
    output_filename = f"{input_path.name}.csv"
    output_path = database_dir / output_filename
    txt_files = list(input_path.glob("*.txt"))
    if not txt_files:
        print(f"Aucun fichier TXT trouvé dans '{input_path}'")
        return
    print(f"Traitement de {len(txt_files)} fichier(s) TXT...")
    
    all_sentences = []
    sentence_id = 1
    
    for txt_file in txt_files:
        if debug:
            print(f"Traitement du fichier: {txt_file.name}")
        
        extractor = SentenceExtractor(txt_file)
        sentences = extractor.extract_sentences()
        
        if debug:
            print(f"  Nombre de phrases extraites: {len(sentences)}")
            if sentences:
                print(f"  Première phrase: {sentences[0][:100]}...")
                print(f"  Dernière phrase: {sentences[-1][:100]}...")
        
        # Ajouter les métadonnées pour chaque phrase
        for sentence in sentences:
            all_sentences.append({
                'sentence_id': sentence_id,
                'text': sentence,
                'source': txt_file.name,
                'vector': ''  # Futur vecteur
            })
            sentence_id += 1
    
    # Écriture du CSV
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
        print(f"CSV créé: {output_path}")
        print(f"Nombre de phrases extraites: {len(all_sentences)}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du CSV: {e}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        process_data(sys.argv[1])
    else:
        print("Usage: python process.py <chemin_vers_dossier>")

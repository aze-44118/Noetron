#!/usr/bin/env python3
"""
Module d'extraction des phrases pour Noetron
"""

import csv
from pathlib import Path
from typing import Union
from processing.txt_processer import SentenceExtractor


def extract_sentences(input_path: Union[str, Path], create_csv: bool = False, debug: bool = False, start_phrase: str = None) -> None:
    """
    Extrait les phrases d'un dossier de fichiers TXT
    Args:
        input_path: Chemin vers le dossier contenant les fichiers TXT
        create_csv: Si True, crée un fichier CSV avec les phrases extraites
        debug: Mode debug pour afficher plus d'informations
        start_phrase: Phrase de départ pour filtrer le contenu (optionnel)
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Erreur: Le dossier '{input_path}' n'existe pas.")
        return
    if not input_path.is_dir():
        print(f"Erreur: '{input_path}' n'est pas un dossier.")
        return
    
    txt_files = list(input_path.glob("*.txt"))
    if not txt_files:
        print(f"Aucun fichier TXT trouvé dans '{input_path}'")
        return
    
    print(f"Extraction des phrases de {len(txt_files)} fichier(s) TXT...")
    
    if start_phrase:
        print(f"🎯 Filtrage à partir de la phrase: '{start_phrase}'")
    
    all_sentences = []
    sentence_id = 1
    
    for txt_file in txt_files:
        if debug:
            print(f"Traitement du fichier: {txt_file.name}")
        
        extractor = SentenceExtractor(txt_file)
        sentences = extractor.extract_sentences(start_phrase=start_phrase)
        
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
                'vector': ''  # Vide pour l'extraction seule
            })
            sentence_id += 1
    
    print(f"Nombre total de phrases extraites: {len(all_sentences)}")
    
    # Créer le CSV si demandé
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
            print(f"CSV créé: {output_path}")
        except Exception as e:
            print(f"Erreur lors de l'écriture du CSV: {e}")
    
    return all_sentences


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        extract_sentences(sys.argv[1], create_csv=True)
    else:
        print("Usage: python extractor.py <chemin_vers_dossier> [--csv]") 
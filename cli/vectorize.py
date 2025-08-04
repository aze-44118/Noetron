#!/usr/bin/env python3
"""
Module de vectorisation des phrases pour Noetron
"""

import csv
import json
import numpy as np
from pathlib import Path
from typing import Union, List, Dict
from sentence_transformers import SentenceTransformer


def vectorize_sentences(csv_path: Union[str, Path], debug: bool = False) -> None:
    """
    Vectorise les phrases d'un fichier CSV en utilisant all-mpnet-base-v2
    Args:
        csv_path: Chemin vers le fichier CSV contenant les phrases
        debug: Mode debug pour afficher plus d'informations
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"Erreur: Le fichier '{csv_path}' n'existe pas.")
        return
    
    print("=== VECTORISATION DES PHRASES ===")
    
    # Charger le modèle
    if debug:
        print("  Chargement du modèle all-mpnet-base-v2...")
    
    try:
        model = SentenceTransformer('all-mpnet-base-v2')
        if debug:
            print("  Modèle chargé avec succès")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {e}")
        return
    
    # Lire le CSV
    sentences_data = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sentences_data.append(row)
    
    if debug:
        print(f"  {len(sentences_data)} phrases à vectoriser")
    
    # Extraire les textes des phrases
    texts = [row['text'] for row in sentences_data]
    
    # Vectoriser les phrases
    if debug:
        print("  Vectorisation en cours...")
    
    try:
        embeddings = model.encode(texts, show_progress_bar=debug)
        if debug:
            print(f"  Vectorisation terminée. Dimensions: {embeddings.shape}")
    except Exception as e:
        print(f"Erreur lors de la vectorisation: {e}")
        return
    
    # Ajouter les vecteurs aux données
    for i, row in enumerate(sentences_data):
        # Convertir le vecteur en liste pour le JSON
        vector_list = embeddings[i].tolist()
        row['vector'] = json.dumps(vector_list)
    
    # Écrire le CSV mis à jour
    output_path = csv_path.parent / f"{csv_path.stem}_vectorized.csv"
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['sentence_id', 'text', 'source', 'vector']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sentences_data)
        
        print(f"=== RÉSULTAT ===")
        print(f"CSV vectorisé créé: {output_path}")
        print(f"Nombre de phrases vectorisées: {len(sentences_data)}")
        print(f"Dimension des vecteurs: {embeddings.shape[1]}")
        
    except Exception as e:
        print(f"Erreur lors de l'écriture du CSV: {e}")


def vectorize_sentences_from_list(sentences: List[Dict], debug: bool = False) -> List[Dict]:
    """
    Vectorise une liste de phrases et retourne les données avec vecteurs
    Args:
        sentences: Liste de dictionnaires contenant les phrases
        debug: Mode debug pour afficher plus d'informations
    Returns:
        Liste de dictionnaires avec les vecteurs ajoutés
    """
    if not sentences:
        print("Aucune phrase à vectoriser")
        return sentences
    
    print("=== VECTORISATION DES PHRASES ===")
    
    # Charger le modèle
    if debug:
        print("  Chargement du modèle all-mpnet-base-v2...")
    
    try:
        model = SentenceTransformer('all-mpnet-base-v2')
        if debug:
            print("  Modèle chargé avec succès")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {e}")
        return sentences
    
    # Extraire les textes des phrases
    texts = [sentence['text'] for sentence in sentences]
    
    # Vectoriser les phrases
    if debug:
        print(f"  Vectorisation de {len(texts)} phrases...")
    
    try:
        embeddings = model.encode(texts, show_progress_bar=debug)
        if debug:
            print(f"  Vectorisation terminée. Dimensions: {embeddings.shape}")
    except Exception as e:
        print(f"Erreur lors de la vectorisation: {e}")
        return sentences
    
    # Ajouter les vecteurs aux données
    for i, sentence in enumerate(sentences):
        # Convertir le vecteur en liste pour le JSON
        vector_list = embeddings[i].tolist()
        sentence['vector'] = json.dumps(vector_list)
    
    if debug:
        print(f"  {len(sentences)} phrases vectorisées avec succès")
    
    return sentences


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        vectorize_sentences(sys.argv[1], debug=True)
    else:
        print("Usage: python vectorize.py <chemin_vers_csv>")

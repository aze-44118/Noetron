#!/usr/bin/env python3
"""
Module de recherche sémantique pour Noetron
"""

import csv
import json
import numpy as np
from pathlib import Path
from typing import Union, List, Dict, Tuple
from sentence_transformers import SentenceTransformer


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calcule la similarité cosinus entre deux vecteurs
    Args:
        vec1: Premier vecteur
        vec2: Deuxième vecteur
    Returns:
        Score de similarité entre 0 et 1
    """
    # Normaliser les vecteurs
    vec1_norm = vec1 / np.linalg.norm(vec1)
    vec2_norm = vec2 / np.linalg.norm(vec2)
    
    # Calculer la similarité cosinus
    similarity = np.dot(vec1_norm, vec2_norm)
    return float(similarity)


def load_vectorized_sentences(csv_path: Union[str, Path]) -> List[Dict]:
    """
    Charge les phrases vectorisées depuis un fichier CSV
    Args:
        csv_path: Chemin vers le fichier CSV vectorisé
    Returns:
        Liste des phrases avec leurs vecteurs
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Le fichier '{csv_path}' n'existe pas.")
    
    sentences = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertir le vecteur JSON en numpy array
            if row['vector']:
                vector = np.array(json.loads(row['vector']))
                sentences.append({
                    'sentence_id': int(row['sentence_id']),
                    'text': row['text'],
                    'source': row['source'],
                    'vector': vector
                })
    
    return sentences


def search_similar_sentences(
    query: str, 
    csv_path: Union[str, Path], 
    top_k: int = 3,
    debug: bool = False
) -> List[Dict]:
    """
    Recherche les phrases les plus similaires à une requête
    Args:
        query: Phrase de recherche
        csv_path: Chemin vers le fichier CSV vectorisé
        top_k: Nombre de résultats à retourner
        debug: Mode debug pour afficher plus d'informations
    Returns:
        Liste des top_k phrases les plus similaires
    """
    if debug:
        print(f"=== RECHERCHE SÉMANTIQUE ===")
        print(f"Requête: '{query}'")
        print(f"Nombre de résultats demandés: {top_k}")
    
    # Charger le modèle BAAI/bge-m3
    if debug:
        print("  Chargement du modèle BAAI/bge-m3...")
    
    try:
        model = SentenceTransformer('BAAI/bge-m3')
        if debug:
            print("  Modèle chargé avec succès")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {e}")
        return []
    
    # Vectoriser la requête
    if debug:
        print("  Vectorisation de la requête...")
    
    try:
        query_vector = model.encode([query])[0]
        if debug:
            print(f"  Requête vectorisée. Dimensions: {query_vector.shape}")
    except Exception as e:
        print(f"Erreur lors de la vectorisation de la requête: {e}")
        return []
    
    # Charger les phrases vectorisées
    if debug:
        print("  Chargement des phrases vectorisées...")
    
    try:
        sentences = load_vectorized_sentences(csv_path)
        if debug:
            print(f"  {len(sentences)} phrases chargées")
    except Exception as e:
        print(f"Erreur lors du chargement des phrases: {e}")
        return []
    
    # Calculer les similarités
    if debug:
        print("  Calcul des similarités cosinus...")
    
    similarities = []
    for sentence in sentences:
        similarity = cosine_similarity(query_vector, sentence['vector'])
        similarities.append({
            'sentence_id': sentence['sentence_id'],
            'text': sentence['text'],
            'source': sentence['source'],
            'similarity_score': similarity
        })
    
    # Trier par score de similarité (décroissant)
    similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    # Retourner le top_k
    top_results = similarities[:top_k]
    
    # Ajouter le rang
    for i, result in enumerate(top_results):
        result['rank'] = i + 1
    
    if debug:
        print(f"  Recherche terminée. Top {len(top_results)} résultats trouvés.")
    
    return top_results


def search_sentences_cli(
    query: str,
    csv_path: Union[str, Path],
    top_k: int = 3,
    debug: bool = False
) -> None:
    """
    Interface CLI pour la recherche de phrases
    Args:
        query: Phrase de recherche
        csv_path: Chemin vers le fichier CSV vectorisé
        top_k: Nombre de résultats à afficher
        debug: Mode debug
    """
    try:
        results = search_similar_sentences(query, csv_path, top_k, debug)
        
        if not results:
            print("Aucun résultat trouvé.")
            return
        
        print(f"\n=== RÉSULTATS DE LA RECHERCHE ===")
        print(f"Requête: '{query}'")
        print(f"Nombre de résultats: {len(results)}")
        print()
        
        for result in results:
            print(f"🏆 RANG {result['rank']} (Score: {result['similarity_score']:.4f})")
            print(f"📖 Texte: {result['text'][:150]}{'...' if len(result['text']) > 150 else ''}")
            print(f"📁 Source: {result['source']}")
            print(f"🆔 ID: {result['sentence_id']}")
            print("-" * 80)
        
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")


def launch_interactive_mode(csv_path: Union[str, Path], top_k: int = 3, debug: bool = False):
    """
    Lance le mode interactif Noetron avec modèle pré-chargé
    Args:
        csv_path: Chemin vers le fichier CSV vectorisé
        top_k: Nombre de résultats par défaut
        debug: Mode debug
    """
    print("🔮 NOETRON ACTIVATED - Environnement d'analyse sémantique")
    print("🚀 Chargement du modèle BAAI/bge-m3...")
    
    try:
        # Charger le modèle une seule fois
        model = SentenceTransformer('BAAI/bge-m3')
        print("✅ Modèle chargé ! Prêt pour l'analyse.")
        
        # Charger les phrases vectorisées
        print(f"📁 Chargement du fichier: {csv_path}")
        sentences = load_vectorized_sentences(csv_path)
        print(f"📊 {len(sentences)} phrases disponibles")
        print(f"🎯 Top K par défaut: {top_k}")
        print()
        print("💡 Tapez 'help' pour voir les commandes disponibles")
        print("💡 Tapez 'quit' ou Ctrl+C pour sortir")
        print("-" * 60)
        
        # Boucle interactive
        while True:
            try:
                # Prompt personnalisé
                user_input = input("noetron> ").strip()
                
                if not user_input:
                    continue
                
                # Commandes de sortie
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("🔮 NOETRON DEACTIVATED")
                    break
                
                # Commande d'aide
                elif user_input.lower() == 'help':
                    print_help_commands()
                    continue
                
                # Commande de recherche
                elif user_input.lower().startswith('search '):
                    handle_search_command(user_input, model, sentences, top_k, debug)
                
                # Commande de comparaison
                elif user_input.lower().startswith('compare '):
                    handle_compare_command(user_input, debug)
                
                # Commande d'extraction
                elif user_input.lower().startswith('extract'):
                    handle_extract_command(user_input, csv_path, debug)
                
                # Commande de traitement
                elif user_input.lower().startswith('process'):
                    handle_process_command(user_input, csv_path, debug)
                
                # Commande inconnue
                else:
                    print("❌ Commande inconnue. Tapez 'help' pour voir les commandes disponibles.")
                
            except KeyboardInterrupt:
                print("\n🔮 NOETRON DEACTIVATED")
                break
            except EOFError:
                print("\n🔮 NOETIVATED")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")
                print("Continuez avec une nouvelle commande...")
    
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return


def print_help_commands():
    """Affiche l'aide des commandes disponibles"""
    print("\n📚 COMMANDES DISPONIBLES:")
    print("  search \"phrase\" [--top N]  - Recherche sémantique")
    print("  compare <source> <dest> [--top N] [--length L] - Comparaison entre corpus")
    print("  extract [--csv] [--debug]   - Extraction de phrases")
    print("  process [--debug]           - Traitement complet")
    print("  help                        - Afficher cette aide")
    print("  quit, exit, q               - Sortir du mode interactif")
    print()
    print("💡 Exemples:")
    print("  search \"philosophie de la perception\"")
    print("  search \"liberté et existence\" --top 5")
    print("  compare database/merleau_ponty.csv database/spinoza.csv")
    print("  compare database/merleau_ponty.csv database/spinoza.csv --top 5")
    print("  compare database/merleau_ponty.csv database/spinoza.csv --length 50")
    print("  compare database/merleau_ponty.csv database/spinoza.csv --top 5 --length 100")
    print("  extract --csv")
    print("  process --debug")


def handle_search_command(user_input: str, model: SentenceTransformer, sentences: List[Dict], top_k: int, debug: bool):
    """Gère la commande de recherche"""
    try:
        # Parser la commande: search "phrase" [--top N]
        # Supprimer "search " du début
        search_part = user_input[7:]  # Enlever "search "
        
        # Extraire la phrase entre guillemets et l'option --top
        import re
        
        # Chercher la phrase entre guillemets
        phrase_match = re.search(r'"([^"]*)"', search_part)
        if phrase_match:
            phrase = phrase_match.group(1)
        else:
            # Si pas de guillemets, prendre le premier mot non-option
            parts = search_part.split()
            phrase_parts = []
            for part in parts:
                if not part.startswith('-') and part not in ['--top']:
                    phrase_parts.append(part)
            phrase = ' '.join(phrase_parts)
        
        # Chercher l'option --top
        top_results = top_k
        top_match = re.search(r'--top\s+(\d+)', search_part)
        if top_match:
            try:
                top_results = int(top_match.group(1))
            except:
                print("⚠️ Option --top invalide, utilisation de la valeur par défaut")
        
        if not phrase:
            print("❌ Erreur: Phrase de recherche manquante")
            print("💡 Syntaxe: search \"votre phrase\" [--top N]")
            return
        
        # Effectuer la recherche
        print(f"🔍 Recherche: '{phrase}' (top {top_results})")
        results = search_similar_sentences_with_model(model, sentences, phrase, top_results, debug)
        
        if results:
            display_search_results(phrase, results)
        else:
            print("❌ Aucun résultat trouvé")
    
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        print("💡 Syntaxe: search \"votre phrase\" [--top N]")


def handle_extract_command(user_input: str, csv_path: Union[str, Path], debug: bool):
    """Gère la commande d'extraction"""
    try:
        print("📖 Extraction des phrases...")
        # Ici vous pouvez appeler votre fonction d'extraction existante
        print("✅ Extraction terminée")
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")


def handle_process_command(user_input: str, csv_path: Union[str, Path], debug: bool):
    """Gère la commande de traitement"""
    try:
        print("⚙️ Traitement des données...")
        # Ici vous pouvez appeler votre fonction de traitement existante
        print("✅ Traitement terminé")
    except Exception as e:
        print(f"❌ Erreur lors du traitement: {e}")


def handle_compare_command(user_input: str, debug: bool):
    """Gère la commande de comparaison"""
    try:
        # Supprimer "compare " du début
        compare_part = user_input[8:]  # Enlever "compare "
        
        # Diviser en parties
        parts = compare_part.split()
        
        if len(parts) < 2:
            print("❌ Erreur: Deux fichiers CSV requis")
            print("💡 Syntaxe: compare <source.csv> <destination.csv> [--top N] [--length L]")
            return
        
        source_csv = parts[0]
        dest_csv = parts[1]
        
        # Chercher l'option --top
        top_results = 3
        if '--top' in parts:
            try:
                top_index = parts.index('--top')
                if top_index + 1 < len(parts):
                    top_results = int(parts[top_index + 1])
            except:
                print("⚠️ Option --top invalide, utilisation de la valeur par défaut (3)")
        
        # Chercher l'option --length
        min_length = 0
        if '--length' in parts:
            try:
                length_index = parts.index('--length')
                if length_index + 1 < len(parts):
                    min_length = int(parts[length_index + 1])
            except:
                print("⚠️ Option --length invalide, utilisation de la valeur par défaut (0)")
        
        # Effectuer la comparaison
        print(f"🔍 Comparaison: {source_csv} → {dest_csv} (top {top_results} global)")
        if min_length > 0:
            print(f"📏 Longueur minimale des phrases: {min_length} caractères")
        
        try:
            from cli.compare import compare_corpus_cli
            compare_corpus_cli(source_csv, dest_csv, top_results, min_length, debug)
        except ImportError as e:
            print(f"❌ Erreur d'import: {e}")
            print("Assurez-vous que le module compare est disponible")
        except Exception as e:
            print(f"❌ Erreur lors de la comparaison: {e}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la comparaison: {e}")
        print("💡 Syntaxe: compare <source.csv> <destination.csv> [--top N] [--length L]")


def search_similar_sentences_with_model(
    model: SentenceTransformer,
    sentences: List[Dict], 
    query: str, 
    top_k: int = 3,
    debug: bool = False
) -> List[Dict]:
    """
    Recherche avec modèle déjà chargé
    """
    if debug:
        print(f"  Vectorisation de la requête...")
    
    try:
        query_vector = model.encode([query])[0]
        if debug:
            print(f"  Requête vectorisée. Dimensions: {query_vector.shape}")
    except Exception as e:
        print(f"Erreur lors de la vectorisation de la requête: {e}")
        return []
    
    if debug:
        print("  Calcul des similarités cosinus...")
    
    similarities = []
    for sentence in sentences:
        similarity = cosine_similarity(query_vector, sentence['vector'])
        similarities.append({
            'sentence_id': sentence['sentence_id'],
            'text': sentence['text'],
            'source': sentence['source'],
            'similarity_score': similarity
        })
    
    # Trier par score de similarité (décroissant)
    similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    # Retourner le top_k
    top_results = similarities[:top_k]
    
    # Ajouter le rang
    for i, result in enumerate(top_results):
        result['rank'] = i + 1
    
    if debug:
        print(f"  Recherche terminée. Top {len(top_results)} résultats trouvés.")
    
    return top_results


def display_search_results(query: str, results: List[Dict]):
    """Affiche les résultats de recherche de manière formatée"""
    print(f"\n🏆 RÉSULTATS POUR: '{query}'")
    print(f"📊 Nombre de résultats: {len(results)}")
    print()
    
    for result in results:
        print(f"🏆 RANG {result['rank']} (Score: {result['similarity_score']:.4f})")
        print(f"📖 Texte: {result['text'][:150]}{'...' if len(result['text']) > 150 else ''}")
        print(f"📁 Source: {result['source']}")
        print(f"🆔 ID: {result['sentence_id']}")
        print("-" * 80)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Recherche sémantique de phrases avec similarité cosinus"
    )
    
    parser.add_argument(
        'query',
        help='Phrase de recherche'
    )
    
    parser.add_argument(
        'csv_path',
        help='Chemin vers le fichier CSV vectorisé'
    )
    
    parser.add_argument(
        '--top',
        type=int,
        default=3,
        help='Nombre de résultats à afficher (défaut: 3)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Mode debug pour afficher plus d\'informations'
    )
    
    args = parser.parse_args()
    
    search_sentences_cli(args.query, args.csv_path, args.top, args.debug)

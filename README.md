# Noetron

Outil de traitement et d'analyse de données avec interface en ligne de commande.

## Installation

1. Cloner le repository :
```bash
git clone <url-du-repo>
cd Noetron
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate     # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Commande `extractor`

Extrait les phrases d'un dossier de fichiers TXT et peut créer un CSV avec les phrases extraites.

#### Fonctionnalités
- **Extraction de phrases** selon des règles spécifiques :
  - **Début de phrase** : majuscule (au début de ligne ou après un point)
  - **Fin de phrase** : point suivi d'une majuscule ou d'un saut de ligne
- **Conversion automatique** en CSV avec une colonne "text"
- **Support multi-fichiers** : traite tous les fichiers `.txt` du dossier

#### Syntaxe
```bash
python cli/main.py extractor -i <nom_du_dossier> [--csv] [--debug]
```

#### Arguments
- `-i, --input` : Nom du dossier à traiter (obligatoire)
  - Si un nom simple est fourni, le dossier sera cherché dans `data/`
  - Si un chemin complet est fourni, il sera utilisé tel quel
- `--csv` : Créer un fichier CSV avec les phrases extraites
- `--debug` : Mode debug pour afficher plus d'informations
- `--start` : Phrase de départ pour filtrer le contenu (ex: "Maurice MERLEAU-PONTY SIGNES")

#### Exemples d'utilisation
```bash
# Extraction simple
python cli/main.py extractor -i mes_textes

# Avec création de CSV
python cli/main.py extractor -i /chemin/vers/dossier --csv

# Avec mode debug
python cli/main.py extractor -i mon_dossier --debug

# Avec phrase de départ (filtrage)
python cli/main.py extractor -i merleau_ponty --start "Maurice MERLEAU-PONTY SIGNES"

# Combinaison d'options
python cli/main.py extractor -i merleau_ponty --start "SIGNES" --csv --debug
```

### Commande `process`

Traite un dossier de fichiers TXT : extraction + vectorisation + autres traitements.

#### Fonctionnalités
- **Extraction de paragraphes** selon des règles spécifiques :
  - **Début de paragraphe** : ligne commençant par une indentation (espaces/tabulations) + majuscule
  - **Fin de paragraphe** : point suivi d'un saut de ligne
- **Conversion automatique** en CSV avec une colonne "text"
- **Support multi-fichiers** : traite tous les fichiers `.txt` du dossier

#### Syntaxe
```bash
python cli/main.py process -i <nom_du_dossier>
```

#### Arguments
- `-i, --input` : Nom du dossier à traiter (obligatoire)
  - Si un nom simple est fourni, le dossier sera cherché dans `data/`
  - Si un chemin complet est fourni, il sera utilisé tel quel

#### Exemples d'utilisation

```bash
# Traiter un dossier dans data/
python cli/main.py process -i mes_textes

# Traiter un dossier avec chemin absolu
python cli/main.py process -i /chemin/complet/vers/dossier

# Utiliser l'alias --input
python cli/main.py process --input documents
```

#### Résultat
- **Fichier CSV créé** : `database/<nom_du_dossier>.csv`
- **Contenu** : Colonnes "sentence_id", "text", "source", "vector"
- **Exemple** : `data/mes_textes/` → `database/mes_textes.csv`

### Commande `vectorize`

Vectorise les phrases d'un fichier CSV en utilisant le modèle BAAI/bge-m3.

#### Fonctionnalités
- **Modèle d'embedding** : BAAI/bge-m3 (multilingue, haute performance)
- **Vectorisation** : Conversion des phrases en vecteurs numériques
- **Format de sortie** : CSV avec colonne "vector" contenant les embeddings

#### Syntaxe
```bash
python cli/vectorize.py <chemin_vers_csv> [--debug]
```

### Commande `search`

Recherche des phrases similaires avec similarité cosinus en utilisant le modèle BAAI/bge-m3.

#### Fonctionnalités
- **Recherche sémantique** : Comprend le sens, pas juste les mots-clés
- **Similarité cosinus** : Calcul précis de la similarité entre vecteurs
- **Top K configurable** : Nombre de résultats personnalisable
- **Scores de confiance** : Affichage des scores de similarité

#### Syntaxe
```bash
python cli/main.py search -p "phrase de recherche" -f <chemin_vers_csv> [--top N] [--debug]
```

#### Arguments
- `-p, --phrase` : Phrase de recherche (obligatoire)
- `-f, --file` : Chemin vers le fichier CSV vectorisé (obligatoire)
- `--top` : Nombre de résultats à afficher (défaut: 3)
- `--debug` : Mode debug pour afficher plus d'informations

#### Exemples d'utilisation
```bash
# Recherche simple
python cli/main.py search -p "La liberté guidant le peuple" -f database/merleau_ponty.csv

# Avec plus de résultats
python cli/main.py search -p "philosophie de la perception" -f database/merleau_ponty.csv --top 5

# Mode debug
python cli/main.py search -p "existence et essence" -f database/merleau_ponty.csv --debug
```

#### Aide
```bash
# Aide générale
python cli/main.py --help

# Aide pour la commande process
python cli/main.py process --help
```

## Structure du projet

```
Noetron/
├── cli/
│   ├── main.py          # Point d'entrée CLI
│   └── process.py       # Orchestration du traitement
├── processing/
│   └── txt_processer.py # Extraction de paragraphes
├── data/                # Dossiers de fichiers TXT à traiter
├── database/            # Fichiers CSV générés
├── vectorization/       # Modules de vectorisation
├── analysis/           # Modules d'analyse
├── tests/              # Tests unitaires
└── requirements.txt    # Dépendances Python
```

## Développement

### Architecture du projet

Le projet suit une architecture modulaire :
- **`cli/`** : Interface en ligne de commande et orchestration
- **`processing/`** : Modules de traitement des données (extraction, nettoyage, etc.)
- **`vectorization/`** : Modules de vectorisation des données
- **`analysis/`** : Modules d'analyse et de traitement avancé

### Ajouter une nouvelle commande

1. Modifier `cli/main.py` pour ajouter un nouveau sous-parser
2. Créer le module correspondant dans le dossier approprié (`processing/`, `vectorization/`, etc.)
3. Importer et utiliser la fonction dans `main.py`

### Ajouter un nouveau processeur

1. Créer une nouvelle classe dans `processing/`
2. Implémenter la logique de traitement spécifique
3. Importer et utiliser dans `cli/process.py` ou créer une nouvelle commande

### Tests

```bash
# Lancer les tests
python -m pytest tests/
```

## Licence

[À définir]

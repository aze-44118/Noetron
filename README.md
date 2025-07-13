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

### Commande `process`

Traite un dossier de fichiers TXT et les convertit en CSV avec extraction de paragraphes.

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
- **Contenu** : Une colonne "text" avec un paragraphe par ligne
- **Exemple** : `data/mes_textes/` → `database/mes_textes.csv`

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

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

Traite un fichier de données avec l'argument `-i` pour spécifier le fichier d'entrée.

#### Syntaxe
```bash
python cli/main.py process -i <nom_du_fichier>
```

#### Arguments
- `-i, --input` : Nom du fichier à traiter (obligatoire)
  - Si un nom simple est fourni, le fichier sera cherché dans le dossier `data/`
  - Si un chemin complet est fourni, il sera utilisé tel quel

#### Exemples d'utilisation

```bash
# Traiter un fichier dans le dossier data
python cli/main.py process -i mon_fichier.txt

# Traiter un fichier avec chemin absolu
python cli/main.py process -i /chemin/complet/vers/fichier.txt

# Utiliser l'alias --input
python cli/main.py process --input donnees.csv
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
│   └── process.py       # Module de traitement
├── data/                # Dossier des fichiers à traiter
├── processing/          # Modules de traitement
├── vectorization/       # Modules de vectorisation
├── analysis/           # Modules d'analyse
├── tests/              # Tests unitaires
└── requirements.txt    # Dépendances Python
```

## Développement

### Ajouter une nouvelle commande

1. Modifier `cli/main.py` pour ajouter un nouveau sous-parser
2. Créer le module correspondant dans le dossier approprié
3. Importer et utiliser la fonction dans `main.py`

### Tests

```bash
# Lancer les tests
python -m pytest tests/
```

## Licence

[À définir]

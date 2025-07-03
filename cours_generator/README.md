# 📚 Générateur automatique de cours en ligne

Système d'automatisation pour créer des cours de français en utilisant l'IA locale (Ollama).

## 🚀 Fonctionnalités

- **Parse automatique** du fichier `francais_all.md` (149 éléments)
- **Génération IA** avec Ollama (Gemma 7B, Mistral 7B, etc.)
- **Templates HTML** basés sur `test_moliere.html`
- **Traitement par batch** avec gestion d'erreurs
- **Optimisation contexte** pour modèles locaux
- **Interface CLI** complète

## 📁 Structure du projet

```
cours_generator/
├── main.py                    # Script principal
├── config.json               # Configuration
├── requirements.txt          # Dépendances Python
├── parsers/
│   ├── __init__.py
│   └── md_parser.py          # Parser francais_all.md
├── generators/
│   ├── __init__.py
│   ├── ollama_client.py      # Client Ollama
│   ├── html_generator.py     # Générateur HTML
│   └── prompt_templates.py   # Templates de prompts
├── templates/
│   └── base_template.html    # Template HTML de base
└── output/
    └── generated_courses/    # Cours générés
```

## 📋 Prérequis

1. **Python 3.8+**
2. **Ollama** installé et configuré
3. **Modèle local** (Gemma 7B recommandé)

### Installation d'Ollama

```bash
# Installation d'Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Téléchargement d'un modèle
ollama pull gemma:7b
# ou
ollama pull mistral:7b
```

## 🔧 Installation

```bash
# Cloner le projet
cd cours_generator/

# Installer les dépendances
pip install -r requirements.txt

# Vérifier qu'Ollama fonctionne
ollama serve
```

## 📖 Utilisation

### Commande de base

```bash
python main.py --input ../francais_all.md --output ./generated_courses
```

### Commande complète

```bash
python main.py \
    --input ../francais_all.md \
    --template ../test.html \
    --output ./generated_courses \
    --model gemma:7b \
    --batch-size 5 \
    --retry 3 \
    --categories auteur mouvement notions
```

### Options disponibles

- `--input, -i` : Fichier francais_all.md (obligatoire)
- `--template, -t` : Template HTML de base
- `--output, -o` : Répertoire de sortie (défaut: output/generated_courses)
- `--model, -m` : Modèle Ollama (défaut: gemma:7b)
- `--batch-size, -b` : Taille des batches (défaut: 5)
- `--retry, -r` : Nombre de tentatives (défaut: 3)
- `--categories, -c` : Catégories à traiter (défaut: toutes)
- `--config` : Fichier de configuration (défaut: config.json)

## 📊 Catégories supportées

- **auteur** (36 éléments) : Biographies d'auteurs
- **mouvement** (15 éléments) : Mouvements littéraires
- **notions** (31 éléments) : Notions littéraires
- **methodes** (7 éléments) : Méthodes d'analyse
- **EAF** (12 éléments) : Épreuves anticipées
- **outils** (8 éléments) : Outils d'analyse
- **Seconde** (13 éléments) : Programme de Seconde
- **Premiere** (17 éléments) : Programme de Première
- **Terminale** (10 éléments) : Programme de Terminale

## ⚙️ Configuration

Le fichier `config.json` permet de personnaliser :

```json
{
    "ollama": {
        "base_url": "http://localhost:11434",
        "model": "gemma:7b",
        "max_tokens": 4096,
        "temperature": 0.7,
        "timeout": 120,
        "retry_count": 3
    },
    "batch_size": 5,
    "output_dir": "output/generated_courses"
}
```

## 🎯 Exemples d'utilisation

### Générer tous les auteurs

```bash
python main.py -i ../francais_all.md -c auteur
```

### Générer avec un modèle spécifique

```bash
python main.py -i ../francais_all.md -m mistral:7b -b 3
```

### Générer les notions et méthodes

```bash
python main.py -i ../francais_all.md -c notions methodes
```

## 📝 Format de sortie

Chaque cours génère un fichier HTML avec :

- **Structure responsive** basée sur test_moliere.html
- **Sommaire navigable** avec ancres
- **Sections thématiques** (présentation, œuvres, style, etc.)
- **Anecdotes et citations** intégrées
- **CSS/JS spécifiques** par catégorie

## 🔍 Tests et validation

### Tester le parser

```bash
cd parsers/
python md_parser.py
```

### Tester Ollama

```bash
cd generators/
python ollama_client.py
```

### Tester la génération HTML

```bash
cd generators/
python html_generator.py
```

## 📈 Monitoring

Le système génère des logs détaillés :

```
cours_generator.log
```

Statistiques disponibles :
- Nombre de requêtes Ollama
- Taux de succès
- Temps de traitement
- Utilisation du cache

## 🐛 Dépannage

### Problèmes courants

1. **Ollama non accessible**
   ```bash
   # Vérifier qu'Ollama fonctionne
   ollama serve
   curl http://localhost:11434/api/tags
   ```

2. **Modèle non disponible**
   ```bash
   # Lister les modèles installés
   ollama list
   
   # Télécharger un modèle
   ollama pull gemma:7b
   ```

3. **Erreurs de parsing**
   ```bash
   # Vérifier le format du fichier
   python parsers/md_parser.py
   ```

### Optimisations

- **Batch size** : Réduire si problèmes de mémoire
- **Timeout** : Augmenter pour modèles lents
- **Cache** : Utilisé automatiquement pour éviter les doublons
- **Retry** : Augmenter si réseau instable

## 🎨 Personnalisation

### Ajouter une catégorie

1. Modifier `parsers/md_parser.py`
2. Ajouter template dans `generators/prompt_templates.py`
3. Créer template HTML dans `generators/html_generator.py`
4. Mettre à jour `config.json`

### Modifier les prompts

Éditer `generators/prompt_templates.py` pour personnaliser :
- Structure des sections
- Ton et style
- Longueur du contenu
- Exemples spécifiques

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Merci de :
1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Consulter les logs pour le débogage
- Vérifier la configuration Ollama
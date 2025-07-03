"""
Templates de prompts pour la génération de contenu éducatif
Optimisés pour les modèles locaux (Gemma 7B, Mistral 7B)
"""

from typing import Dict, Any, Optional
import json


class PromptTemplates:
    """Gestionnaire des templates de prompts"""
    
    def __init__(self):
        self.base_system_prompt = """Tu es un assistant spécialisé dans la création de contenu éducatif pour des cours de français.
Tu dois créer du contenu structuré, clair et engageant pour des lycéens français.
Ton style doit être :
- Pédagogique mais pas ennuyeux
- Avec des anecdotes pertinentes
- Structuré et facile à comprendre
- Respectueux du niveau scolaire français
- Avec des exemples concrets

Réponds uniquement avec le contenu demandé, sans préambule ni commentaires."""
    
    def get_prompt(self, category: str, item: Dict[str, Any]) -> str:
        """Génère un prompt adapté à la catégorie et l'élément"""
        if category == 'auteur':
            return self._get_auteur_prompt(item)
        elif category == 'mouvement':
            return self._get_mouvement_prompt(item)
        elif category == 'notions':
            return self._get_notion_prompt(item)
        elif category == 'methodes':
            return self._get_methode_prompt(item)
        elif category == 'EAF':
            return self._get_eaf_prompt(item)
        elif category == 'outils':
            return self._get_outil_prompt(item)
        else:
            return self._get_generic_prompt(item, category)
    
    def _get_auteur_prompt(self, item: Dict[str, Any]) -> str:
        """Prompt pour les auteurs"""
        name = item.get('name', 'Auteur inconnu')
        
        return f"""Crée un contenu complet sur l'auteur {name} pour un cours de français lycée.

STRUCTURE OBLIGATOIRE :
1. **Présentation express** (2-3 phrases accrocheuses)
2. **Repères clés** (dates importantes, contexte historique)
3. **Œuvres majeures** (5-7 œuvres principales avec année et genre)
4. **Style et thèmes** (caractéristiques littéraires, innovations)
5. **Citations célèbres** (3-4 citations emblématiques)
6. **Anecdotes** (3-4 anecdotes intéressantes mais véridiques)

CONSIGNES :
- Niveau lycée (Seconde à Terminale)
- Ton engageant mais sérieux
- Anecdotes authentiques seulement
- Exemples concrets d'œuvres
- Contextualisation historique
- Maximum 800 mots total

EXEMPLE DE TON : "Molière, c'est le roi incontesté de la comédie française ! Ce génie du théâtre..."

Commence directement par le contenu, sans introduction."""
    
    def _get_mouvement_prompt(self, item: Dict[str, Any]) -> str:
        """Prompt pour les mouvements littéraires"""
        name = item.get('name', 'Mouvement inconnu')
        
        return f"""Crée un contenu pédagogique sur le mouvement littéraire "{name}" pour lycéens.

STRUCTURE OBLIGATOIRE :
1. **Définition** (Qu'est-ce que c'est en 2-3 phrases)
2. **Contexte historique** (Époque, causes, événements)
3. **Caractéristiques** (Thèmes, style, innovations)
4. **Auteurs principaux** (5-6 auteurs représentatifs)
5. **Œuvres emblématiques** (4-5 œuvres clés)
6. **Héritage** (Influence sur la littérature suivante)

CONSIGNES :
- Explications claires et accessibles
- Liens avec l'histoire et la société
- Exemples précis d'œuvres
- Différences avec les autres mouvements
- Maximum 700 mots

EXEMPLE DE TON : "Le romantisme, c'est la révolution des sentiments dans la littérature..."

Commence directement par le contenu."""
    
    def _get_notion_prompt(self, item: Dict[str, Any]) -> str:
        """Prompt pour les notions littéraires"""
        name = item.get('name', 'Notion inconnue')
        
        return f"""Explique la notion littéraire "{name}" pour des lycéens français.

STRUCTURE OBLIGATOIRE :
1. **Définition simple** (En 1-2 phrases claires)
2. **Explication détaillée** (Comment ça marche, à quoi ça sert)
3. **Types et variantes** (Différentes formes si applicable)
4. **Exemples concrets** (Extraits d'œuvres au programme)
5. **Méthode d'analyse** (Comment repérer et analyser)
6. **Pièges à éviter** (Erreurs fréquentes des élèves)

CONSIGNES :
- Définition précise et compréhensible
- Exemples tirés des œuvres classiques
- Méthode pratique d'application
- Liens avec l'analyse littéraire
- Maximum 600 mots

EXEMPLE DE TON : "La métaphore, c'est comme un déguisement pour les mots..."

Commence directement par le contenu."""
    
    def _get_methode_prompt(self, item: Dict[str, Any]) -> str:
        """Prompt pour les méthodes"""
        name = item.get('name', 'Méthode inconnue')
        
        return f"""Crée un guide méthodologique sur "{name}" pour lycéens.

STRUCTURE OBLIGATOIRE :
1. **Objectif** (À quoi sert cette méthode)
2. **Étapes détaillées** (Process étape par étape)
3. **Conseils pratiques** (Astuces pour réussir)
4. **Exemple concret** (Application sur un cas réel)
5. **Critères d'évaluation** (Ce qu'attend le correcteur)
6. **Erreurs à éviter** (Pièges fréquents)

CONSIGNES :
- Instructions claires et applicables
- Exemple d'application concrète
- Conseils pour l'examen
- Méthode progressive
- Maximum 700 mots

EXEMPLE DE TON : "Le commentaire, c'est comme démonter une horloge pour comprendre comment elle marche..."

Commence directement par le contenu."""
    
    def _get_eaf_prompt(self, item: Dict[str, Any]) -> str:
        """Prompt pour les EAF (Épreuves Anticipées de Français)"""
        name = item.get('name', 'Épreuve inconnue')
        
        return f"""Crée un guide pour l'épreuve "{name}" du baccalauréat français.

STRUCTURE OBLIGATOIRE :
1. **Présentation de l'épreuve** (Format, durée, coefficient)
2. **Compétences évaluées** (Ce qu'on attend de l'élève)
3. **Méthodologie** (Étapes à suivre)
4. **Conseils stratégiques** (Gestion du temps, priorités)
5. **Exemples types** (Cas concrets d'application)
6. **Préparation** (Comment s'entraîner efficacement)

CONSIGNES :
- Informations officielles et à jour
- Conseils pratiques et applicables
- Exemples d'épreuves réelles
- Stratégies anti-stress
- Maximum 800 mots

EXEMPLE DE TON : "L'entretien oral, c'est votre moment de briller..."

Commence directement par le contenu."""
    
    def _get_outil_prompt(self, item: Dict[str, Any]) -> str:
        """Prompt pour les outils"""
        name = item.get('name', 'Outil inconnu')
        
        return f"""Présente l'outil "{name}" pour l'analyse littéraire au lycée.

STRUCTURE OBLIGATOIRE :
1. **Définition** (Qu'est-ce que c'est)
2. **Utilité** (À quoi ça sert concrètement)
3. **Mode d'emploi** (Comment l'utiliser)
4. **Exemples d'application** (Cas pratiques)
5. **Conseils d'utilisation** (Bonnes pratiques)
6. **Compléments** (Autres outils connexes)

CONSIGNES :
- Explication claire et pratique
- Exemples concrets d'utilisation
- Conseils méthodologiques
- Applications dans les exercices
- Maximum 600 mots

EXEMPLE DE TON : "Le plan dialectique, c'est votre boussole pour structurer votre pensée..."

Commence directement par le contenu."""
    
    def _get_generic_prompt(self, item: Dict[str, Any], category: str) -> str:
        """Prompt générique pour les autres catégories"""
        name = item.get('name', 'Élément inconnu')
        
        return f"""Crée un contenu éducatif sur "{name}" (catégorie: {category}) pour lycéens.

STRUCTURE OBLIGATOIRE :
1. **Introduction** (Présentation générale)
2. **Développement** (Explication détaillée)
3. **Exemples** (Cas concrets et applications)
4. **Conseils pratiques** (Utilisation en cours/examen)
5. **Synthèse** (Points clés à retenir)

CONSIGNES :
- Adaptation au niveau lycée
- Contenu précis et vérifiable
- Exemples du programme scolaire
- Ton pédagogique et engageant
- Maximum 700 mots

Commence directement par le contenu."""
    
    def get_system_prompt(self, category: str) -> str:
        """Retourne le prompt système adapté à la catégorie"""
        return self.base_system_prompt
    
    def optimize_prompt_length(self, prompt: str, max_length: int = 3000) -> str:
        """Optimise la longueur d'un prompt"""
        if len(prompt) <= max_length:
            return prompt
        
        # Garder l'essentiel: structure + consignes
        lines = prompt.split('\n')
        important_lines = []
        
        for line in lines:
            if any(keyword in line.upper() for keyword in ['STRUCTURE', 'CONSIGNES', 'EXEMPLE']):
                important_lines.append(line)
            elif line.strip() and not line.startswith('EXEMPLE DE TON'):
                important_lines.append(line)
        
        optimized = '\n'.join(important_lines)
        
        if len(optimized) > max_length:
            # Dernière réduction
            optimized = optimized[:max_length-50] + "\n\nCommence directement par le contenu."
        
        return optimized


def main():
    """Test des templates"""
    templates = PromptTemplates()
    
    # Test avec différents types d'éléments
    test_items = [
        {'category': 'auteur', 'item': {'name': 'Victor Hugo'}},
        {'category': 'mouvement', 'item': {'name': 'Romantisme'}},
        {'category': 'notions', 'item': {'name': 'Métaphore'}},
        {'category': 'methodes', 'item': {'name': 'Commentaire'}},
    ]
    
    for test in test_items:
        print(f"\n{'='*50}")
        print(f"CATÉGORIE: {test['category'].upper()}")
        print(f"ÉLÉMENT: {test['item']['name']}")
        print(f"{'='*50}")
        
        prompt = templates.get_prompt(test['category'], test['item'])
        print(f"Longueur: {len(prompt)} caractères")
        print(f"Prompt:\n{prompt[:200]}...")


if __name__ == "__main__":
    main()
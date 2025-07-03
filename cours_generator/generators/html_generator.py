"""
Générateur HTML pour les cours
Basé sur le template test_moliere.html
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json


class HTMLGenerator:
    """Générateur de pages HTML pour les cours"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_template_path = config.get('base_template', 'templates/base_template.html')
        
        # Templates par catégorie
        self.category_templates = {
            'auteur': self._get_auteur_template,
            'mouvement': self._get_mouvement_template,
            'notions': self._get_notion_template,
            'methodes': self._get_methode_template,
            'EAF': self._get_eaf_template,
            'outils': self._get_outil_template,
        }
        
        # CSS par catégorie
        self.category_css = {
            'auteur': 'auteur.test1.css',
            'mouvement': 'mouvement.css',
            'notions': 'notions.css',
            'methodes': 'methodes.css',
            'EAF': 'eaf.css',
            'outils': 'outils.css',
            'Seconde': 'seconde.css',
            'Premiere': 'premiere.css',
            'Terminale': 'terminale.css'
        }
    
    def generate_html(self, category: str, item: Dict[str, Any], generated_content: str) -> str:
        """Génère le HTML complet pour un cours"""
        # Parsing du contenu généré
        parsed_content = self._parse_generated_content(generated_content)
        
        # Sélection du template
        template_func = self.category_templates.get(category, self._get_generic_template)
        
        # Génération HTML
        html_content = template_func(item, parsed_content)
        
        return html_content
    
    def _parse_generated_content(self, content: str) -> Dict[str, str]:
        """Parse le contenu généré par l'IA en sections"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Détection des sections (headers avec **)
            if line.startswith('**') and line.endswith('**'):
                # Sauvegarder la section précédente
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Nouvelle section
                current_section = line.strip('*').strip().lower()
                current_content = []
            else:
                current_content.append(line)
        
        # Sauvegarder la dernière section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _get_auteur_template(self, item: Dict[str, Any], content: Dict[str, str]) -> str:
        """Template pour les auteurs"""
        name = item.get('name', 'Auteur inconnu')
        name_formatted = self._format_name(name)
        
        # Extraction des informations
        presentation = content.get('présentation express', content.get('présentation', ''))
        reperes = content.get('repères clés', content.get('repères', ''))
        oeuvres = content.get('œuvres majeures', content.get('oeuvres', ''))
        style = content.get('style et thèmes', content.get('style', ''))
        citations = content.get('citations célèbres', content.get('citations', ''))
        anecdotes = content.get('anecdotes', '')
        
        # Génération du sommaire
        sommaire = self._generate_sommaire([
            ('presentation', '📜 Présentation'),
            ('reperes', '🕰️ Repères'),
            ('oeuvres', '📚 Œuvres'),
            ('style', '🎨 Style'),
            ('citations', '✍️ Citations'),
            ('anecdotes', '🎭 Anecdotes'),
            ('nexschool', '🚀 NexSchool')
        ])
        
        # Image de l'auteur
        image_url = item.get('url', 'https://via.placeholder.com/300x400?text=Portrait')
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexSkool - {name_formatted}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/{self.category_css.get('auteur', 'auteur.css')}">
</head>
<body>

<div class="nexskool-markdown">
    <div class="markdown-content">

        <!-- TITRE PRINCIPAL -->
        <h1>📚 {name_formatted}</h1>

        <!-- ZONE SOMMAIRE + IMAGE -->
        <div class="zone-sommaire-et-image">
            <div class="bloc-gauche">
                <nav class="sommaire">
                    {sommaire}
                </nav>
                <div class="phrase-accroche">
                    <em>"{self._extract_quote(presentation)}"</em>
                </div>
            </div>

            <div class="zone-image-portrait">
                <img class="portrait-auteur" src="{image_url}" alt="Portrait de {name_formatted}" />
            </div>
        </div>

        <!-- SECTIONS -->
        {self._generate_section('presentation', '📜 Présentation express', presentation)}
        {self._generate_section('reperes', '🕰️ Repères clés', reperes)}
        {self._generate_section('oeuvres', '📚 Œuvres majeures', oeuvres)}
        {self._generate_section('style', '🎨 Style & thèmes', style)}
        {self._generate_section('citations', '✍️ Citations incontournables', citations)}
        {self._generate_section('anecdotes', '🎭 Anecdotes croustillantes', anecdotes)}
        {self._generate_nexschool_section(name_formatted)}

    </div>
</div>

<script src="/js/auteur.test1.js"></script>

</body>
</html>"""
        
        return html
    
    def _get_mouvement_template(self, item: Dict[str, Any], content: Dict[str, str]) -> str:
        """Template pour les mouvements littéraires"""
        name = item.get('name', 'Mouvement inconnu')
        name_formatted = self._format_name(name)
        
        # Extraction des informations
        definition = content.get('définition', '')
        contexte = content.get('contexte historique', content.get('contexte', ''))
        caracteristiques = content.get('caractéristiques', '')
        auteurs = content.get('auteurs principaux', content.get('auteurs', ''))
        oeuvres = content.get('œuvres emblématiques', content.get('oeuvres', ''))
        heritage = content.get('héritage', '')
        
        sommaire = self._generate_sommaire([
            ('definition', '📖 Définition'),
            ('contexte', '🏛️ Contexte'),
            ('caracteristiques', '🎨 Caractéristiques'),
            ('auteurs', '👥 Auteurs'),
            ('oeuvres', '📚 Œuvres'),
            ('heritage', '🌟 Héritage')
        ])
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexSkool - {name_formatted}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/{self.category_css.get('mouvement', 'mouvement.css')}">
</head>
<body>

<div class="nexskool-markdown">
    <div class="markdown-content">

        <h1>🎭 {name_formatted}</h1>

        <div class="zone-sommaire-et-image">
            <div class="bloc-gauche">
                <nav class="sommaire">
                    {sommaire}
                </nav>
                <div class="phrase-accroche">
                    <em>"{self._extract_quote(definition)}"</em>
                </div>
            </div>
        </div>

        {self._generate_section('definition', '📖 Définition', definition)}
        {self._generate_section('contexte', '🏛️ Contexte historique', contexte)}
        {self._generate_section('caracteristiques', '🎨 Caractéristiques', caracteristiques)}
        {self._generate_section('auteurs', '👥 Auteurs principaux', auteurs)}
        {self._generate_section('oeuvres', '📚 Œuvres emblématiques', oeuvres)}
        {self._generate_section('heritage', '🌟 Héritage', heritage)}

    </div>
</div>

<script src="/js/mouvement.js"></script>

</body>
</html>"""
        
        return html
    
    def _get_notion_template(self, item: Dict[str, Any], content: Dict[str, str]) -> str:
        """Template pour les notions littéraires"""
        name = item.get('name', 'Notion inconnue')
        name_formatted = self._format_name(name)
        
        definition = content.get('définition simple', content.get('définition', ''))
        explication = content.get('explication détaillée', content.get('explication', ''))
        types = content.get('types et variantes', content.get('types', ''))
        exemples = content.get('exemples concrets', content.get('exemples', ''))
        methode = content.get('méthode d\'analyse', content.get('méthode', ''))
        pieges = content.get('pièges à éviter', content.get('pièges', ''))
        
        sommaire = self._generate_sommaire([
            ('definition', '📖 Définition'),
            ('explication', '🔍 Explication'),
            ('types', '📝 Types'),
            ('exemples', '💡 Exemples'),
            ('methode', '🎯 Méthode'),
            ('pieges', '⚠️ Pièges')
        ])
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexSkool - {name_formatted}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/{self.category_css.get('notions', 'notions.css')}">
</head>
<body>

<div class="nexskool-markdown">
    <div class="markdown-content">

        <h1>🔍 {name_formatted}</h1>

        <div class="zone-sommaire-et-image">
            <div class="bloc-gauche">
                <nav class="sommaire">
                    {sommaire}
                </nav>
                <div class="phrase-accroche">
                    <em>"{self._extract_quote(definition)}"</em>
                </div>
            </div>
        </div>

        {self._generate_section('definition', '📖 Définition', definition)}
        {self._generate_section('explication', '🔍 Explication détaillée', explication)}
        {self._generate_section('types', '📝 Types et variantes', types)}
        {self._generate_section('exemples', '💡 Exemples concrets', exemples)}
        {self._generate_section('methode', '🎯 Méthode d\'analyse', methode)}
        {self._generate_section('pieges', '⚠️ Pièges à éviter', pieges)}

    </div>
</div>

<script src="/js/notions.js"></script>

</body>
</html>"""
        
        return html
    
    def _get_methode_template(self, item: Dict[str, Any], content: Dict[str, str]) -> str:
        """Template pour les méthodes"""
        name = item.get('name', 'Méthode inconnue')
        name_formatted = self._format_name(name)
        
        objectif = content.get('objectif', '')
        etapes = content.get('étapes détaillées', content.get('étapes', ''))
        conseils = content.get('conseils pratiques', content.get('conseils', ''))
        exemple = content.get('exemple concret', content.get('exemple', ''))
        criteres = content.get('critères d\'évaluation', content.get('critères', ''))
        erreurs = content.get('erreurs à éviter', content.get('erreurs', ''))
        
        sommaire = self._generate_sommaire([
            ('objectif', '🎯 Objectif'),
            ('etapes', '📋 Étapes'),
            ('conseils', '💡 Conseils'),
            ('exemple', '📝 Exemple'),
            ('criteres', '📊 Critères'),
            ('erreurs', '⚠️ Erreurs')
        ])
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexSkool - {name_formatted}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/{self.category_css.get('methodes', 'methodes.css')}">
</head>
<body>

<div class="nexskool-markdown">
    <div class="markdown-content">

        <h1>🎯 {name_formatted}</h1>

        <div class="zone-sommaire-et-image">
            <div class="bloc-gauche">
                <nav class="sommaire">
                    {sommaire}
                </nav>
                <div class="phrase-accroche">
                    <em>"{self._extract_quote(objectif)}"</em>
                </div>
            </div>
        </div>

        {self._generate_section('objectif', '🎯 Objectif', objectif)}
        {self._generate_section('etapes', '📋 Étapes détaillées', etapes)}
        {self._generate_section('conseils', '💡 Conseils pratiques', conseils)}
        {self._generate_section('exemple', '📝 Exemple concret', exemple)}
        {self._generate_section('criteres', '📊 Critères d\'évaluation', criteres)}
        {self._generate_section('erreurs', '⚠️ Erreurs à éviter', erreurs)}

    </div>
</div>

<script src="/js/methodes.js"></script>

</body>
</html>"""
        
        return html
    
    def _get_eaf_template(self, item: Dict[str, Any], content: Dict[str, str]) -> str:
        """Template pour les EAF"""
        return self._get_generic_template(item, content, 'EAF')
    
    def _get_outil_template(self, item: Dict[str, Any], content: Dict[str, str]) -> str:
        """Template pour les outils"""
        return self._get_generic_template(item, content, 'outils')
    
    def _get_generic_template(self, item: Dict[str, Any], content: Dict[str, str], category: str = 'generic') -> str:
        """Template générique"""
        name = item.get('name', 'Élément inconnu')
        name_formatted = self._format_name(name)
        
        # Utiliser toutes les sections disponibles
        sections = []
        for key, value in content.items():
            if value.strip():
                sections.append((key.replace(' ', '_'), self._format_section_title(key), value))
        
        # Générer le sommaire
        sommaire_items = [(section[0], section[1]) for section in sections]
        sommaire = self._generate_sommaire(sommaire_items)
        
        # Générer les sections
        sections_html = '\n'.join([
            self._generate_section(section[0], section[1], section[2])
            for section in sections
        ])
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexSkool - {name_formatted}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/{self.category_css.get(category, 'generic.css')}">
</head>
<body>

<div class="nexskool-markdown">
    <div class="markdown-content">

        <h1>📚 {name_formatted}</h1>

        <div class="zone-sommaire-et-image">
            <div class="bloc-gauche">
                <nav class="sommaire">
                    {sommaire}
                </nav>
                <div class="phrase-accroche">
                    <em>"{self._extract_quote(list(content.values())[0] if content else '')}"</em>
                </div>
            </div>
        </div>

        {sections_html}

    </div>
</div>

<script src="/js/{category}.js"></script>

</body>
</html>"""
        
        return html
    
    def _generate_sommaire(self, items: list) -> str:
        """Génère le HTML du sommaire"""
        sommaire_items = []
        for item_id, title in items:
            sommaire_items.append(f'<a href="#{item_id}">{title}</a>')
        return '\n                    '.join(sommaire_items)
    
    def _generate_section(self, section_id: str, title: str, content: str) -> str:
        """Génère une section HTML"""
        if not content.strip():
            return ''
        
        # Formatage du contenu
        formatted_content = self._format_content(content)
        
        return f"""
        <div class="section-block" id="{section_id}">
            <summary>{title}</summary>
            <div class="contenu-section">
                {formatted_content}
            </div>
        </div>"""
    
    def _generate_nexschool_section(self, name: str) -> str:
        """Génère la section NexSchool"""
        return f"""
        <div class="section-block" id="nexschool">
            <summary>🚀 Conseil NexSchool</summary>
            <div class="contenu-section">
                <div class="NexSchool">
                    🧠 <strong>Méthode :</strong> Pour retenir {name}, utilisez la méthode des associations visuelles et des anecdotes marquantes !
                </div>
                
                <div class="alert alert-info">
                    💡 <strong>Astuce de révision :</strong> Créez une fiche avec les points clés et relisez-la régulièrement !
                </div>
            </div>
        </div>"""
    
    def _format_content(self, content: str) -> str:
        """Formate le contenu avec les balises HTML appropriées"""
        # Remplacer les listes à puces
        content = re.sub(r'^- (.+)', r'<li>\1</li>', content, flags=re.MULTILINE)
        content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', content, flags=re.DOTALL)
        
        # Remplacer les paragraphes
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                if not para.startswith('<'):
                    para = f'<p>{para}</p>'
                formatted_paragraphs.append(para)
        
        return '\n\n                '.join(formatted_paragraphs)
    
    def _format_name(self, name: str) -> str:
        """Formate le nom pour l'affichage"""
        return name.replace('_', ' ').title()
    
    def _format_section_title(self, title: str) -> str:
        """Formate le titre d'une section"""
        return title.replace('_', ' ').title()
    
    def _extract_quote(self, text: str) -> str:
        """Extrait une citation du texte"""
        if not text:
            return "Une référence incontournable"
        
        # Chercher une phrase entre guillemets
        quote_match = re.search(r'"([^"]+)"', text)
        if quote_match:
            return quote_match.group(1)
        
        # Sinon, prendre la première phrase
        first_sentence = text.split('.')[0].strip()
        if len(first_sentence) > 60:
            first_sentence = first_sentence[:60] + '...'
        
        return first_sentence if first_sentence else "Une référence incontournable"


def main():
    """Test du générateur HTML"""
    generator = HTMLGenerator({'base_template': 'test_template.html'})
    
    # Test avec un auteur
    item = {
        'name': 'moliere',
        'url': 'https://example.com/moliere.jpg'
    }
    
    content = {
        'présentation express': 'Molière est le maître de la comédie française. Il a révolutionné le théâtre.',
        'repères clés': '1622: Naissance\n1659: Premier succès\n1673: Mort',
        'œuvres majeures': 'Tartuffe, Dom Juan, Le Misanthrope, L\'Avare',
        'style et thèmes': 'Comédie de caractère, satire sociale, respect des règles classiques',
        'citations célèbres': '"Il faut manger pour vivre et non pas vivre pour manger"',
        'anecdotes': 'Il est mort en scène en jouant Le Malade imaginaire'
    }
    
    html = generator.generate_html('auteur', item, content)
    print("HTML généré avec succès!")
    print(f"Longueur: {len(html)} caractères")


if __name__ == "__main__":
    main()
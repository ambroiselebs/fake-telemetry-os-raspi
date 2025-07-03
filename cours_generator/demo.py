#!/usr/bin/env python3
"""
Script de démonstration du générateur de cours
Teste tous les composants sans faire d'appels à Ollama
"""

import json
import asyncio
from pathlib import Path

from parsers.md_parser import FrancaisParser
from generators.html_generator import HTMLGenerator
from generators.prompt_templates import PromptTemplates


async def demo_parser():
    """Démonstration du parser"""
    print("="*60)
    print("🔍 DÉMONSTRATION DU PARSER")
    print("="*60)
    
    parser = FrancaisParser()
    
    try:
        # Parse du fichier francais_all.md
        data = parser.parse_file('../francais_all.md')
        stats = parser.get_statistics(data)
        
        print(f"\n📊 STATISTIQUES:")
        print(f"   • Total d'éléments: {stats['total_items']}")
        print(f"   • Existants: {stats['existing_items']}")
        print(f"   • À créer: {stats['to_create_items']}")
        print(f"   • Catégories: {stats['categories']}")
        
        print(f"\n📂 DÉTAIL PAR CATÉGORIE:")
        for category, items in data.items():
            print(f"\n   {category.upper()} ({len(items)} éléments):")
            for item in items[:3]:  # Afficher les 3 premiers
                status_emoji = "✅" if item.status == "exists" else "🔄"
                print(f"      {status_emoji} {item.name}")
            if len(items) > 3:
                print(f"      ... et {len(items) - 3} autres")
        
        print(f"\n✅ Parser testé avec succès!")
        return data
        
    except Exception as e:
        print(f"❌ Erreur du parser: {e}")
        return None


def demo_prompts():
    """Démonstration des templates de prompts"""
    print("\n" + "="*60)
    print("📝 DÉMONSTRATION DES PROMPTS")
    print("="*60)
    
    templates = PromptTemplates()
    
    # Test avec différents types d'éléments
    test_items = [
        {'category': 'auteur', 'item': {'name': 'Victor Hugo'}},
        {'category': 'mouvement', 'item': {'name': 'Romantisme'}},
        {'category': 'notions', 'item': {'name': 'Métaphore'}},
        {'category': 'methodes', 'item': {'name': 'Commentaire'}},
    ]
    
    for test in test_items:
        print(f"\n📋 CATÉGORIE: {test['category'].upper()}")
        print(f"   Élément: {test['item']['name']}")
        
        prompt = templates.get_prompt(test['category'], test['item'])
        print(f"   Longueur: {len(prompt)} caractères")
        print(f"   Début: {prompt[:100]}...")
    
    print(f"\n✅ Templates de prompts testés!")


def demo_html_generator():
    """Démonstration du générateur HTML"""
    print("\n" + "="*60)
    print("🎨 DÉMONSTRATION DU GÉNÉRATEUR HTML")
    print("="*60)
    
    generator = HTMLGenerator({'base_template': 'templates/base_template.html'})
    
    # Contenu simulé généré par l'IA
    mock_content = {
        'présentation express': 'Molière est le maître incontesté de la comédie française! Ce génie du théâtre a révolutionné la scène avec ses personnages inoubliables et sa critique sociale féroce.',
        'repères clés': '1622: Naissance de Jean-Baptiste Poquelin\n1643: Création de l\'Illustre Théâtre\n1659: Premier succès avec "Les Précieuses ridicules"\n1666: "Le Misanthrope"\n1673: Mort en scène',
        'œuvres majeures': 'Tartuffe (1664) - Critique la fausse dévotion\nDom Juan (1665) - Le libertin face à la mort\nLe Misanthrope (1666) - L\'homme qui déteste les hommes\nL\'Avare (1668) - Harpagon et sa cassette\nLe Bourgeois gentilhomme (1670) - M. Jourdain fait de la prose',
        'style et thèmes': 'Molière crée la comédie de caractère avec des personnages aux défauts exagérés. Il respecte les règles classiques tout en les dynamitant de l\'intérieur. Son secret: faire rire tout en faisant réfléchir!',
        'citations célèbres': '"Il faut manger pour vivre et non pas vivre pour manger"\n"On ne meurt qu\'une fois, et c\'est pour si longtemps!"\n"Le devoir d\'une femme est de paraître joyeuse"',
        'anecdotes': 'Molière a épousé Armande Béjart, qui était soit la sœur, soit la fille de sa maîtresse! Il crachait du sang le soir de sa mort mais a continué à jouer jusqu\'au bout. "Tartuffe" a été interdite 5 ans car trop subversive.'
    }
    
    # Test avec un auteur
    item = {
        'name': 'moliere',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/1/17/Moliere.jpg'
    }
    
    # Simulation du contenu généré
    generated_content = '\n'.join([
        f"**{key}**\n{value}\n"
        for key, value in mock_content.items()
    ])
    
    html = generator.generate_html('auteur', item, generated_content)
    
    # Sauvegarde du fichier de démonstration
    demo_path = Path('output/demo_moliere.html')
    demo_path.parent.mkdir(exist_ok=True)
    
    with open(demo_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n📄 HTML généré:")
    print(f"   • Longueur: {len(html)} caractères")
    print(f"   • Sections: {len(mock_content)} sections")
    print(f"   • Fichier sauvé: {demo_path}")
    print(f"   • Ouvrir avec: firefox {demo_path}")
    
    print(f"\n✅ Générateur HTML testé!")


def demo_config():
    """Démonstration de la configuration"""
    print("\n" + "="*60)
    print("⚙️ DÉMONSTRATION DE LA CONFIGURATION")
    print("="*60)
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"\n📋 Configuration actuelle:")
        print(f"   • Modèle Ollama: {config['ollama']['model']}")
        print(f"   • URL Ollama: {config['ollama']['base_url']}")
        print(f"   • Batch size: {config['batch_size']}")
        print(f"   • Répertoire de sortie: {config['output_dir']}")
        print(f"   • Timeout: {config['ollama']['timeout']}s")
        print(f"   • Retry count: {config['ollama']['retry_count']}")
        
        print(f"\n📂 Catégories activées:")
        for category, settings in config['categories'].items():
            status = "✅" if settings['enabled'] else "❌"
            print(f"   {status} {category} (CSS: {settings['css']})")
        
        print(f"\n✅ Configuration chargée!")
        
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")


async def demo_complete():
    """Démonstration complète"""
    print("🚀 DÉMONSTRATION COMPLÈTE DU GÉNÉRATEUR DE COURS")
    print("="*60)
    
    # Test du parser
    parsed_data = await demo_parser()
    
    # Test des prompts
    demo_prompts()
    
    # Test du générateur HTML
    demo_html_generator()
    
    # Test de la configuration
    demo_config()
    
    print("\n" + "="*60)
    print("🎯 RÉSUMÉ DE LA DÉMONSTRATION")
    print("="*60)
    
    if parsed_data:
        stats = FrancaisParser().get_statistics(parsed_data)
        print(f"\n✅ Système prêt pour traiter {stats['total_items']} éléments")
        print(f"   • Parser: ✅ Opérationnel")
        print(f"   • Prompts: ✅ Configurés")
        print(f"   • HTML Generator: ✅ Fonctionnel")
        print(f"   • Configuration: ✅ Chargée")
        
        print(f"\n🚀 COMMANDES POUR DÉMARRER:")
        print(f"   • Test complet: python demo.py")
        print(f"   • Génération réelle: python main.py -i ../francais_all.md")
        print(f"   • Aide: python main.py --help")
        
    else:
        print(f"\n❌ Problème détecté - vérifier le fichier francais_all.md")
    
    print(f"\n📚 Prochaines étapes:")
    print(f"   1. Installer et démarrer Ollama")
    print(f"   2. Télécharger un modèle (ollama pull gemma:7b)")
    print(f"   3. Lancer la génération")
    print(f"   4. Vérifier les fichiers HTML générés")


if __name__ == "__main__":
    asyncio.run(demo_complete())
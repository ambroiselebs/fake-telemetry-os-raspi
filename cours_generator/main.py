#!/usr/bin/env python3
"""
Générateur automatique de cours en ligne
Utilise Ollama pour générer du contenu éducatif à partir de francais_all.md
"""

import asyncio
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from parsers.md_parser import FrancaisParser
from generators.ollama_client import OllamaClient
from generators.html_generator import HTMLGenerator
from generators.prompt_templates import PromptTemplates


class CourseGenerator:
    """Générateur principal de cours"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.parser = FrancaisParser()
        self.ollama = OllamaClient(config.get('ollama', {}))
        self.html_generator = HTMLGenerator(config.get('templates', {}))
        self.prompt_templates = PromptTemplates()
        
        # Configuration des logs
        self.setup_logging()
    
    def setup_logging(self):
        """Configuration du système de logs"""
        log_level = self.config.get('logging', {}).get('level', 'INFO')
        log_file = self.config.get('logging', {}).get('file', 'cours_generator.log')
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def generate_course(self, category: str, item: Dict) -> Optional[str]:
        """Génère un cours pour un élément donné"""
        try:
            self.logger.info(f"Génération de {category}/{item['name']}")
            
            # Génération du prompt basé sur la catégorie
            prompt = self.prompt_templates.get_prompt(category, item)
            
            # Génération du contenu avec Ollama
            content = await self.ollama.generate_content(prompt)
            if not content:
                self.logger.error(f"Échec génération contenu pour {item['name']}")
                return None
            
            # Génération HTML
            html_content = self.html_generator.generate_html(
                category, item, content
            )
            
            # Sauvegarde
            output_path = self.get_output_path(category, item['name'])
            await self.save_course(output_path, html_content)
            
            self.logger.info(f"Cours généré: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Erreur génération {item['name']}: {str(e)}")
            return None
    
    def get_output_path(self, category: str, name: str) -> Path:
        """Détermine le chemin de sortie pour un cours"""
        output_dir = Path(self.config.get('output_dir', 'output/generated_courses'))
        return output_dir / category / f"{name}.html"
    
    async def save_course(self, path: Path, content: str):
        """Sauvegarde un cours généré"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    async def process_batch(self, items: List[tuple], batch_size: int = 5):
        """Traite un lot d'éléments en parallèle"""
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            self.logger.info(f"Traitement batch {i//batch_size + 1}/{len(items)//batch_size + 1}")
            
            tasks = [
                self.generate_course(category, item)
                for category, item in batch
            ]
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch_results)
            
            # Pause entre les batches pour éviter la surcharge
            await asyncio.sleep(1)
        
        return results
    
    async def run(self, input_file: str, categories: Optional[List[str]] = None):
        """Lance la génération complète"""
        self.logger.info(f"Début génération à partir de {input_file}")
        
        # Parsing du fichier d'entrée
        parsed_data = self.parser.parse_file(input_file)
        if not parsed_data:
            self.logger.error("Échec du parsing")
            return
        
        # Préparation des éléments à traiter
        items_to_process = []
        for category, items in parsed_data.items():
            if categories and category not in categories:
                continue
            for item in items:
                items_to_process.append((category, item))
        
        self.logger.info(f"Nombre total d'éléments: {len(items_to_process)}")
        
        # Traitement par batches
        batch_size = self.config.get('batch_size', 5)
        results = await self.process_batch(items_to_process, batch_size)
        
        # Rapport final
        successful = sum(1 for r in results if r and not isinstance(r, Exception))
        self.logger.info(f"Génération terminée: {successful}/{len(items_to_process)} succès")


def load_config(config_file: str) -> Dict:
    """Charge la configuration depuis un fichier JSON"""
    if Path(config_file).exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='Générateur automatique de cours')
    parser.add_argument('--input', '-i', required=True, help='Fichier francais_all.md')
    parser.add_argument('--template', '-t', help='Template HTML de base')
    parser.add_argument('--output', '-o', default='output/generated_courses', help='Répertoire de sortie')
    parser.add_argument('--model', '-m', default='gemma:7b', help='Modèle Ollama')
    parser.add_argument('--batch-size', '-b', type=int, default=5, help='Taille des batches')
    parser.add_argument('--retry', '-r', type=int, default=3, help='Nombre de tentatives')
    parser.add_argument('--categories', '-c', nargs='+', help='Catégories à traiter')
    parser.add_argument('--config', default='config.json', help='Fichier de configuration')
    
    args = parser.parse_args()
    
    # Configuration
    config = load_config(args.config)
    config.update({
        'output_dir': args.output,
        'batch_size': args.batch_size,
        'retry_count': args.retry,
        'ollama': {
            'model': args.model,
            'base_url': config.get('ollama', {}).get('base_url', 'http://localhost:11434')
        },
        'templates': {
            'base_template': args.template or 'templates/base_template.html'
        }
    })
    
    # Lancement
    generator = CourseGenerator(config)
    asyncio.run(generator.run(args.input, args.categories))


if __name__ == "__main__":
    main()
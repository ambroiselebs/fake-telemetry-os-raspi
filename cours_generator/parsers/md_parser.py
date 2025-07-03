"""
Parser pour extraire les données du fichier francais_all.md
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, NamedTuple


class CourseItem(NamedTuple):
    """Représente un élément de cours"""
    name: str
    filename: str
    status: str  # 'exists', 'to_create', 'unknown'
    url: Optional[str] = None
    category: Optional[str] = None


class FrancaisParser:
    """Parser pour le fichier francais_all.md"""
    
    def __init__(self):
        self.categories = {
            'auteur': 'Auteurs',
            'mouvement': 'Mouvements littéraires',
            'notions': 'Notions littéraires',
            'methodes': 'Méthodes',
            'EAF': 'Épreuves anticipées',
            'outils': 'Outils',
            'Seconde': 'Classe de Seconde',
            'Premiere': 'Classe de Première',
            'Terminale': 'Classe de Terminale'
        }
    
    def parse_file(self, file_path: str) -> Dict[str, List[CourseItem]]:
        """Parse le fichier francais_all.md et extrait tous les éléments"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_content(content)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
        except Exception as e:
            raise Exception(f"Erreur lors du parsing: {str(e)}")
    
    def _parse_content(self, content: str) -> Dict[str, List[CourseItem]]:
        """Parse le contenu du fichier markdown"""
        result = {}
        
        # Diviser le contenu par sections
        sections = self._split_by_sections(content)
        
        for section_name, section_content in sections.items():
            if section_name in self.categories:
                items = self._parse_section(section_name, section_content)
                result[section_name] = items
        
        return result
    
    def _split_by_sections(self, content: str) -> Dict[str, str]:
        """Divise le contenu en sections basées sur les répertoires"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # Détection d'une nouvelle section
            if line.startswith('/') and line.endswith('/'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                
                current_section = line.strip('/')
                current_content = []
            else:
                current_content.append(line)
        
        # Ajouter la dernière section
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _parse_section(self, section_name: str, content: str) -> List[CourseItem]:
        """Parse une section spécifique"""
        items = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('│') or line.startswith('├──') or line.startswith('└──'):
                continue
            
            # Parsing des différents types de lignes
            if line.startswith('├──') or line.startswith('└──'):
                item = self._parse_item_line(line, section_name)
                if item:
                    items.append(item)
            elif '.md' in line:
                item = self._parse_md_line(line, section_name)
                if item:
                    items.append(item)
            elif '/' in line and not line.startswith('#'):
                # Sous-répertoires (comme pour Seconde, Premiere, Terminale)
                sub_items = self._parse_subdirectory(line, section_name)
                items.extend(sub_items)
        
        return items
    
    def _parse_item_line(self, line: str, category: str) -> Optional[CourseItem]:
        """Parse une ligne avec ├── ou └──"""
        # Nettoyer la ligne
        clean_line = re.sub(r'^[├└]──\s*', '', line)
        
        # Extraire le nom du fichier
        if '.md' in clean_line:
            parts = clean_line.split()
            filename = parts[0]
            name = filename.replace('.md', '').replace('_', ' ')
            
            # Détecter le statut et l'URL
            status = 'exists'
            url = None
            
            if '(à créer)' in clean_line:
                status = 'to_create'
                # Chercher une URL
                url_match = re.search(r'https?://[^\s]+', clean_line)
                if url_match:
                    url = url_match.group(0)
            
            return CourseItem(
                name=name,
                filename=filename,
                status=status,
                url=url,
                category=category
            )
        
        return None
    
    def _parse_md_line(self, line: str, category: str) -> Optional[CourseItem]:
        """Parse une ligne contenant .md"""
        # Extraire le nom du fichier
        md_match = re.search(r'(\w+\.md)', line)
        if md_match:
            filename = md_match.group(1)
            name = filename.replace('.md', '').replace('_', ' ')
            
            # Détecter le statut
            status = 'exists'
            url = None
            
            if '(à créer)' in line:
                status = 'to_create'
                url_match = re.search(r'https?://[^\s]+', line)
                if url_match:
                    url = url_match.group(0)
            
            return CourseItem(
                name=name,
                filename=filename,
                status=status,
                url=url,
                category=category
            )
        
        return None
    
    def _parse_subdirectory(self, line: str, category: str) -> List[CourseItem]:
        """Parse les sous-répertoires (pour Seconde, Premiere, Terminale)"""
        items = []
        
        # Pour l'instant, on retourne une liste vide
        # Cette fonction peut être étendue pour parser les sous-structures
        
        return items
    
    def get_statistics(self, parsed_data: Dict[str, List[CourseItem]]) -> Dict[str, int]:
        """Retourne des statistiques sur les données parsées"""
        stats = {
            'total_items': 0,
            'existing_items': 0,
            'to_create_items': 0,
            'categories': len(parsed_data)
        }
        
        for category, items in parsed_data.items():
            stats['total_items'] += len(items)
            for item in items:
                if item.status == 'exists':
                    stats['existing_items'] += 1
                elif item.status == 'to_create':
                    stats['to_create_items'] += 1
        
        return stats
    
    def filter_by_status(self, parsed_data: Dict[str, List[CourseItem]], 
                        status: str) -> Dict[str, List[CourseItem]]:
        """Filtre les données par statut"""
        filtered = {}
        
        for category, items in parsed_data.items():
            filtered_items = [item for item in items if item.status == status]
            if filtered_items:
                filtered[category] = filtered_items
        
        return filtered
    
    def get_items_by_category(self, parsed_data: Dict[str, List[CourseItem]], 
                            category: str) -> List[CourseItem]:
        """Retourne les éléments d'une catégorie spécifique"""
        return parsed_data.get(category, [])


def main():
    """Test du parser"""
    parser = FrancaisParser()
    
    # Test avec le fichier francais_all.md
    try:
        data = parser.parse_file('../francais_all.md')
        stats = parser.get_statistics(data)
        
        print("=== STATISTIQUES ===")
        print(f"Total d'éléments: {stats['total_items']}")
        print(f"Existants: {stats['existing_items']}")
        print(f"À créer: {stats['to_create_items']}")
        print(f"Catégories: {stats['categories']}")
        
        print("\n=== DÉTAIL PAR CATÉGORIE ===")
        for category, items in data.items():
            print(f"\n{category.upper()} ({len(items)} éléments):")
            for item in items[:5]:  # Afficher les 5 premiers
                print(f"  - {item.name} ({item.status})")
            if len(items) > 5:
                print(f"  ... et {len(items) - 5} autres")
    
    except Exception as e:
        print(f"Erreur: {e}")


if __name__ == "__main__":
    main()
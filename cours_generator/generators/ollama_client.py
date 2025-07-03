"""
Client pour l'API Ollama
Gère les appels au modèle local et l'optimisation du contexte
"""

import aiohttp
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


class OllamaClient:
    """Client pour communiquer avec Ollama"""
    
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.model = config.get('model', 'gemma:7b')
        self.max_tokens = config.get('max_tokens', 4096)
        self.temperature = config.get('temperature', 0.7)
        self.retry_count = config.get('retry_count', 3)
        self.timeout = config.get('timeout', 120)
        
        self.logger = logging.getLogger(__name__)
        
        # Cache pour éviter les appels répétés
        self.cache = {}
        
        # Statistiques
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'total_tokens': 0
        }
    
    async def generate_content(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        """Génère du contenu avec le modèle Ollama"""
        # Vérifier le cache
        cache_key = self._get_cache_key(prompt, system_prompt)
        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            self.logger.info("Résultat trouvé dans le cache")
            return self.cache[cache_key]
        
        self.stats['total_requests'] += 1
        
        # Préparation de la requête
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': self.temperature,
                'num_predict': self.max_tokens
            }
        }
        
        if system_prompt:
            payload['system'] = system_prompt
        
        # Tentatives avec retry
        for attempt in range(self.retry_count):
            try:
                result = await self._make_request(payload)
                if result:
                    self.stats['successful_requests'] += 1
                    self.cache[cache_key] = result
                    return result
                
            except Exception as e:
                self.logger.warning(f"Tentative {attempt + 1} échouée: {str(e)}")
                if attempt < self.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # Backoff exponentiel
        
        self.stats['failed_requests'] += 1
        self.logger.error(f"Échec de génération après {self.retry_count} tentatives")
        return None
    
    async def _make_request(self, payload: Dict) -> Optional[str]:
        """Effectue la requête HTTP vers Ollama"""
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    
                    if response.status != 200:
                        self.logger.error(f"Erreur HTTP {response.status}: {await response.text()}")
                        return None
                    
                    result = await response.json()
                    
                    if 'response' in result:
                        content = result['response'].strip()
                        
                        # Mise à jour des stats
                        if 'eval_count' in result:
                            self.stats['total_tokens'] += result['eval_count']
                        
                        return content
                    
                    self.logger.error(f"Réponse invalide: {result}")
                    return None
        
        except asyncio.TimeoutError:
            self.logger.error("Timeout lors de la requête")
            return None
        except Exception as e:
            self.logger.error(f"Erreur lors de la requête: {str(e)}")
            return None
    
    def _get_cache_key(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Génère une clé de cache unique"""
        content = f"{self.model}:{prompt}"
        if system_prompt:
            content += f":{system_prompt}"
        return str(hash(content))
    
    async def check_model_availability(self) -> bool:
        """Vérifie si le modèle est disponible"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        models = await response.json()
                        available_models = [m['name'] for m in models.get('models', [])]
                        return self.model in available_models
            
            return False
        
        except Exception as e:
            self.logger.error(f"Erreur vérification modèle: {str(e)}")
            return False
    
    def optimize_prompt(self, prompt: str, max_length: int = 3000) -> str:
        """Optimise un prompt pour respecter la limite de tokens"""
        if len(prompt) <= max_length:
            return prompt
        
        # Stratégie simple: garder le début et la fin
        half_length = max_length // 2
        truncated = prompt[:half_length] + "\n[...]\n" + prompt[-half_length:]
        
        self.logger.info(f"Prompt tronqué de {len(prompt)} à {len(truncated)} caractères")
        return truncated
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'utilisation"""
        return {
            **self.stats,
            'cache_size': len(self.cache),
            'success_rate': self.stats['successful_requests'] / max(1, self.stats['total_requests']) * 100
        }
    
    def clear_cache(self):
        """Vide le cache"""
        self.cache.clear()
        self.logger.info("Cache vidé")
    
    async def test_connection(self) -> bool:
        """Test la connexion avec Ollama"""
        try:
            test_prompt = "Dis bonjour en français."
            result = await self.generate_content(test_prompt)
            return result is not None
        
        except Exception as e:
            self.logger.error(f"Test de connexion échoué: {str(e)}")
            return False


class PromptOptimizer:
    """Optimiseur de prompts pour les modèles locaux"""
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.logger = logging.getLogger(__name__)
    
    def chunk_content(self, content: str, chunk_size: int = 2000) -> List[str]:
        """Divise le contenu en chunks gérables"""
        chunks = []
        words = content.split()
        
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                    current_length = len(word)
                else:
                    # Mot trop long, on le garde quand même
                    chunks.append(word)
                    current_length = 0
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def estimate_tokens(self, text: str) -> int:
        """Estime le nombre de tokens (approximation)"""
        # Approximation: 1 token ≈ 4 caractères pour le français
        return len(text) // 4
    
    def optimize_for_model(self, prompt: str, available_tokens: int) -> str:
        """Optimise un prompt pour un nombre de tokens disponible"""
        estimated_tokens = self.estimate_tokens(prompt)
        
        if estimated_tokens <= available_tokens:
            return prompt
        
        # Réduction proportionnelle
        reduction_ratio = available_tokens / estimated_tokens
        target_length = int(len(prompt) * reduction_ratio)
        
        # Stratégie: garder le début (instructions) et une partie du contenu
        if target_length < 200:
            return prompt[:target_length]
        
        # Garder les 200 premiers caractères (instructions) et le reste du contenu
        instructions = prompt[:200]
        remaining_length = target_length - 200
        content = prompt[200:]
        
        if len(content) <= remaining_length:
            return prompt
        
        # Prendre le début et la fin du contenu
        half_remaining = remaining_length // 2
        optimized_content = content[:half_remaining] + "\n[...]\n" + content[-half_remaining:]
        
        return instructions + optimized_content


async def main():
    """Test du client Ollama"""
    config = {
        'base_url': 'http://localhost:11434',
        'model': 'gemma:7b',
        'max_tokens': 2048,
        'temperature': 0.7
    }
    
    client = OllamaClient(config)
    
    # Test de connexion
    print("Test de connexion...")
    if await client.test_connection():
        print("✅ Connexion réussie!")
    else:
        print("❌ Échec de connexion")
        return
    
    # Test de génération
    print("\nTest de génération...")
    prompt = "Explique brièvement qui était Molière en 50 mots maximum."
    result = await client.generate_content(prompt)
    
    if result:
        print(f"✅ Génération réussie:\n{result}")
    else:
        print("❌ Échec de génération")
    
    # Statistiques
    print(f"\nStatistiques: {client.get_stats()}")


if __name__ == "__main__":
    asyncio.run(main())
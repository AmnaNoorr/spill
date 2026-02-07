"""TF-IDF similarity detection service (FR-7.4)"""

import logging
import re
from typing import Dict, List, Tuple
from collections import Counter
import math
from utils.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class SimilarityService:
    """Service for detecting duplicate rumors using TF-IDF"""
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
            'had', 'what', 'said', 'each', 'which', 'their', 'time', 'if',
            'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her',
            'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'very',
            'after', 'words', 'long', 'than', 'first', 'its', 'who', 'been',
            'oil', 'sit', 'now', 'find', 'down', 'day', 'did', 'get', 'come',
            'made', 'may', 'part'
        }
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
        
        Returns:
            List of lowercase words (no stop words)
        """
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove stop words and short words
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        
        return words
    
    def calculate_tf(self, words: List[str]) -> Dict[str, float]:
        """
        Calculate Term Frequency (TF)
        
        Args:
            words: List of words
        
        Returns:
            Dictionary mapping words to their TF scores
        """
        word_count = Counter(words)
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        tf = {word: count / total_words for word, count in word_count.items()}
        return tf
    
    def calculate_idf(self, all_documents: List[List[str]]) -> Dict[str, float]:
        """
        Calculate Inverse Document Frequency (IDF)
        
        Args:
            all_documents: List of tokenized documents
        
        Returns:
            Dictionary mapping words to their IDF scores
        """
        total_docs = len(all_documents)
        if total_docs == 0:
            return {}
        
        # Count documents containing each word
        doc_frequency = Counter()
        for doc in all_documents:
            unique_words = set(doc)
            doc_frequency.update(unique_words)
        
        # Calculate IDF
        idf = {}
        for word, doc_count in doc_frequency.items():
            idf[word] = math.log(total_docs / (1 + doc_count))
        
        return idf
    
    def calculate_tfidf(self, words: List[str], idf: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate TF-IDF for a document
        
        Args:
            words: Tokenized words
            idf: IDF scores
        
        Returns:
            Dictionary mapping words to their TF-IDF scores
        """
        tf = self.calculate_tf(words)
        tfidf = {word: tf[word] * idf.get(word, 0) for word in tf.keys()}
        return tfidf
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Calculate cosine similarity between two TF-IDF vectors
        
        Args:
            vec1: First TF-IDF vector
            vec2: Second TF-IDF vector
        
        Returns:
            Cosine similarity score (0-1)
        """
        # Get all unique words
        all_words = set(vec1.keys()) | set(vec2.keys())
        
        if not all_words:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in all_words)
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]
    
    def check_duplicate_tfidf(self, text: str, threshold: float = 0.7) -> Dict:
        """
        Check if text is a duplicate using TF-IDF (FR-7.4)
        
        Args:
            text: Text to check for duplicates
            threshold: Similarity threshold (default 0.7)
        
        Returns:
            Dictionary with is_duplicate, similar_to, similarity, similar_text
        """
        try:
            # Tokenize input text
            input_words = self.tokenize(text)
            
            if not input_words:
                return {
                    'is_duplicate': False,
                    'similar_to': None,
                    'similarity': 0.0,
                    'similar_text': None
                }
            
            # Get all active markets
            supabase = get_supabase_client()
            markets_response = supabase.table('markets').select('id, text').eq('status', 'active').execute()
            
            if not markets_response.data:
                return {
                    'is_duplicate': False,
                    'similar_to': None,
                    'similarity': 0.0,
                    'similar_text': None
                }
            
            # Tokenize all existing markets
            all_documents = []
            market_texts = {}
            for market in markets_response.data:
                market_id = market.get('id')
                market_text = market.get('text', '')
                market_words = self.tokenize(market_text)
                if market_words:  # Only add non-empty documents
                    all_documents.append(market_words)
                    market_texts[market_id] = market_words
            
            if not all_documents:
                return {
                    'is_duplicate': False,
                    'similar_to': None,
                    'similarity': 0.0,
                    'similar_text': None
                }
            
            # Add input document for IDF calculation
            all_documents.append(input_words)
            
            # Calculate IDF for all documents
            idf = self.calculate_idf(all_documents)
            
            # Calculate TF-IDF for input text
            input_tfidf = self.calculate_tfidf(input_words, idf)
            
            # Find most similar market
            max_similarity = 0.0
            most_similar_market_id = None
            most_similar_text = None
            
            for market_id, market_words in market_texts.items():
                market_tfidf = self.calculate_tfidf(market_words, idf)
                similarity = self.cosine_similarity(input_tfidf, market_tfidf)
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_market_id = market_id
                    # Get original text
                    for market in markets_response.data:
                        if market.get('id') == market_id:
                            most_similar_text = market.get('text')
                            break
            
            is_duplicate = max_similarity >= threshold
            
            return {
                'is_duplicate': is_duplicate,
                'similar_to': most_similar_market_id if is_duplicate else None,
                'similarity': round(float(max_similarity), 4),
                'similar_text': most_similar_text if is_duplicate else None
            }
            
        except Exception as e:
            logger.error(f"Error in check_duplicate_tfidf: {str(e)}")
            return {
                'is_duplicate': False,
                'similar_to': None,
                'similarity': 0.0,
                'similar_text': None,
                'error': str(e)
            }



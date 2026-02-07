"""AI service for OpenAI integration"""

import os
import json
import logging
import numpy as np
from openai import OpenAI
from config import Config
from utils.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI operations using OpenAI"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY') or Config.OPENAI_API_KEY
        self.client = OpenAI(api_key=api_key) if api_key else None
    
    def generate_prediction(self, market_data, user_query=None):
        """Generate market prediction using AI"""
        if not self.client:
            return None, "OpenAI API key not configured"
        
        try:
            prompt = self._build_prompt(market_data, user_query)
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial market prediction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            prediction = response.choices[0].message.content
            return prediction, None
        except Exception as e:
            return None, str(e)
    
    def _build_prompt(self, market_data, user_query):
        """Build prompt for AI prediction"""
        base_prompt = f"Analyze the following market data and provide a prediction:\n\n{market_data}\n\n"
        if user_query:
            base_prompt += f"User question: {user_query}\n\n"
        base_prompt += "Provide a concise prediction with reasoning."
        return base_prompt
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        if not self.client:
            return None, "OpenAI API key not configured"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Respond with only: positive, negative, or neutral."},
                    {"role": "user", "content": f"Analyze the sentiment of: {text}"}
                ],
                temperature=0.3,
                max_tokens=10
            )
            sentiment = response.choices[0].message.content.strip().lower()
            return sentiment, None
        except Exception as e:
            logger.error(f"Error in analyze_sentiment: {str(e)}")
            return None, str(e)
    
    def classify_rumor(self, text: str) -> dict:
        """
        Classify campus rumor as TRUE/FALSE/UNCERTAIN with confidence and reason
        
        Args:
            text: The rumor text to classify
        
        Returns:
            Dictionary with prediction, confidence, and reasoning
        """
        if not self.client:
            logger.warning("OpenAI client not available, returning fallback")
            return {
                'prediction': 'UNCERTAIN',
                'confidence': 50,
                'reasoning': 'AI unavailable'
            }
        
        try:
            prompt = f"""Classify this campus rumor as TRUE, FALSE, or UNCERTAIN. 
Provide your response as JSON with the following structure:
{{
    "prediction": "TRUE|FALSE|UNCERTAIN",
    "confidence": <number 0-100>,
    "reasoning": "<brief explanation>"
}}

Rumor: {text}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing campus rumors. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # Validate and normalize
            prediction = result.get('prediction', 'UNCERTAIN').upper()
            if prediction not in ['TRUE', 'FALSE', 'UNCERTAIN']:
                prediction = 'UNCERTAIN'
            
            confidence = int(result.get('confidence', 50))
            confidence = max(0, min(100, confidence))  # Clamp to 0-100
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'reasoning': result.get('reasoning', 'No reasoning provided')
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in classify_rumor: {str(e)}")
            return {
                'prediction': 'UNCERTAIN',
                'confidence': 50,
                'reasoning': 'AI unavailable'
            }
        except Exception as e:
            logger.error(f"Error in classify_rumor: {str(e)}")
            return {
                'prediction': 'UNCERTAIN',
                'confidence': 50,
                'reasoning': 'AI unavailable'
            }
    
    def check_duplicate(self, text: str) -> dict:
        """
        Check if text is a duplicate of existing markets using embedding similarity
        
        Args:
            text: The text to check for duplicates
        
        Returns:
            Dictionary with is_duplicate, similar_to, similarity, similar_text
        """
        try:
            # Generate embedding for new text
            new_embedding = self.generate_embedding(text)
            if not new_embedding:
                return {
                    'is_duplicate': False,
                    'similar_to': None,
                    'similarity': 0.0,
                    'similar_text': None
                }
            
            new_embedding = np.array(new_embedding)
            
            # Get all active markets with embeddings
            supabase = get_supabase_client()
            markets_response = supabase.table('markets').select('id, text, embedding').eq('status', 'active').not_.is_('embedding', 'null').execute()
            
            if not markets_response.data:
                return {
                    'is_duplicate': False,
                    'similar_to': None,
                    'similarity': 0.0,
                    'similar_text': None
                }
            
            max_similarity = 0.0
            most_similar_market = None
            most_similar_text = None
            
            for market in markets_response.data:
                if not market.get('embedding'):
                    continue
                
                existing_embedding = np.array(market['embedding'])
                similarity = self.cosine_similarity(new_embedding, existing_embedding)
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_market = market.get('id')
                    most_similar_text = market.get('text')
            
            is_duplicate = max_similarity > 0.85
            
            return {
                'is_duplicate': is_duplicate,
                'similar_to': most_similar_market if is_duplicate else None,
                'similarity': round(float(max_similarity), 4),
                'similar_text': most_similar_text if is_duplicate else None
            }
            
        except Exception as e:
            logger.error(f"Error in check_duplicate: {str(e)}")
            return {
                'is_duplicate': False,
                'similar_to': None,
                'similarity': 0.0,
                'similar_text': None
            }
    
    def generate_embedding(self, text: str) -> list:
        """
        Generate embedding vector for text
        
        Args:
            text: Text to generate embedding for
        
        Returns:
            Embedding vector as list, or None on failure
        """
        if not self.client:
            logger.warning("OpenAI client not available for embedding")
            return None
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error in generate_embedding: {str(e)}")
            return None
    
    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            a: First vector
            b: Second vector
        
        Returns:
            Cosine similarity as float
        """
        try:
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            return dot_product / (norm_a * norm_b)
        except Exception as e:
            logger.error(f"Error in cosine_similarity: {str(e)}")
            return 0.0
    
    def summarize_evidence(self, links: list, rumor: str) -> str:
        """
        Summarize evidence from links about a rumor
        
        Args:
            links: List of URLs or text sources
            rumor: The rumor text
        
        Returns:
            1-2 sentence summary, or fallback message
        """
        if not self.client:
            return "Unable to summarize"
        
        try:
            links_text = "\n".join([f"- {link}" for link in links])
            prompt = f"""Summarize the following sources about this rumor. Provide 1-2 sentences.

Rumor: {rumor}

Sources:
{links_text}

Summary:"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at summarizing evidence. Be concise and factual."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            summary = response.choices[0].message.content.strip()
            return summary if summary else "Unable to summarize"
            
        except Exception as e:
            logger.error(f"Error in summarize_evidence: {str(e)}")
            return "Unable to summarize"


"""Automated evidence fetching service (FR-5.2)"""

import logging
import re
from typing import List, Dict, Optional
from urllib.parse import urlparse
import requests
from services.ai_service import AIService

logger = logging.getLogger(__name__)

class EvidenceService:
    """Service for automated evidence fetching from public sources"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid
        
        Args:
            url: URL string
        
        Returns:
            True if valid URL
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def fetch_url_content(self, url: str, timeout: int = 10) -> Optional[Dict]:
        """
        Fetch content from URL
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
        
        Returns:
            Dictionary with content, title, and metadata, or None on failure
        """
        try:
            if not self.is_valid_url(url):
                return None
            
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            
            # Extract text content
            if 'text/html' in content_type:
                # Simple HTML text extraction (remove tags)
                text = re.sub(r'<[^>]+>', ' ', response.text)
                text = re.sub(r'\s+', ' ', text).strip()
                
                # Try to extract title
                title_match = re.search(r'<title[^>]*>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else None
                if title:
                    title = re.sub(r'\s+', ' ', title)
            elif 'application/json' in content_type:
                try:
                    data = response.json()
                    text = str(data)
                    title = None
                except:
                    text = response.text[:1000]  # Limit text length
                    title = None
            else:
                text = response.text[:2000]  # Limit text length
                title = None
            
            return {
                'url': url,
                'title': title,
                'content': text[:5000],  # Limit content length
                'content_type': content_type,
                'status_code': response.status_code,
                'success': True
            }
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch URL {url}: {str(e)}")
            return {
                'url': url,
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return {
                'url': url,
                'success': False,
                'error': str(e)
            }
    
    def fetch_multiple_urls(self, urls: List[str]) -> List[Dict]:
        """
        Fetch content from multiple URLs
        
        Args:
            urls: List of URLs to fetch
        
        Returns:
            List of fetched content dictionaries
        """
        results = []
        for url in urls:
            if not url or not isinstance(url, str):
                continue
            
            result = self.fetch_url_content(url)
            if result:
                results.append(result)
        
        return results
    
    def extract_evidence_from_urls(self, urls: List[str], rumor_text: str) -> Dict:
        """
        Extract and summarize evidence from URLs related to a rumor
        
        Args:
            urls: List of URLs to fetch
            rumor_text: The rumor text to check against
        
        Returns:
            Dictionary with evidence summary and relevance
        """
        try:
            # Fetch all URLs
            fetched_content = self.fetch_multiple_urls(urls)
            
            if not fetched_content:
                return {
                    'success': False,
                    'error': 'No valid URLs or failed to fetch content',
                    'evidence_count': 0
                }
            
            # Use AI to summarize and check relevance
            evidence_texts = []
            for item in fetched_content:
                if item.get('success') and item.get('content'):
                    evidence_texts.append({
                        'url': item.get('url'),
                        'title': item.get('title', 'No title'),
                        'content': item.get('content', '')[:1000]  # Limit for AI processing
                    })
            
            if not evidence_texts:
                return {
                    'success': False,
                    'error': 'No valid content extracted from URLs',
                    'evidence_count': 0
                }
            
            # Generate summary using AI
            summary = None
            if self.ai_service.client:
                try:
                    # Create prompt for evidence analysis
                    evidence_list = "\n\n".join([
                        f"URL: {e['url']}\nTitle: {e['title']}\nContent: {e['content'][:500]}"
                        for e in evidence_texts
                    ])
                    
                    prompt = f"""Analyze the following evidence sources about this rumor. Provide a 2-3 sentence summary of what the evidence shows.

Rumor: {rumor_text}

Evidence Sources:
{evidence_list}

Summary:"""
                    
                    response = self.ai_service.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are an expert at analyzing evidence. Be concise and factual."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=200
                    )
                    
                    summary = response.choices[0].message.content.strip()
                except Exception as e:
                    logger.warning(f"Failed to generate AI summary: {str(e)}")
            
            return {
                'success': True,
                'evidence_count': len(evidence_texts),
                'sources': evidence_texts,
                'ai_summary': summary or 'Unable to generate summary',
                'urls_processed': len(urls),
                'urls_successful': len([e for e in fetched_content if e.get('success')])
            }
            
        except Exception as e:
            logger.error(f"Error extracting evidence: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'evidence_count': 0
            }
    
    def auto_fetch_evidence(self, market_id: str, rumor_text: str) -> Dict:
        """
        Automatically fetch evidence for a market (for automated oracle bots)
        
        Args:
            market_id: Market ID
            rumor_text: The rumor text
        
        Returns:
            Dictionary with fetched evidence
        """
        # This is a placeholder for automated evidence fetching
        # In production, this could:
        # 1. Search web for related news/articles
        # 2. Check official sources (university websites, etc.)
        # 3. Use APIs to fetch public data
        # 4. Return structured evidence
        
        logger.info(f"Auto-fetching evidence for market {market_id}")
        
        # For now, return a structure that can be extended
        return {
            'success': False,
            'message': 'Automated evidence fetching not fully implemented',
            'market_id': market_id,
            'suggestions': [
                'Implement web search API integration',
                'Add university/official source checking',
                'Add news API integration'
            ]
        }


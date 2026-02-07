"""Market service for business logic"""

from typing import Dict
from utils.supabase_client import get_supabase_client
from models.market import Market
from models.user import User

class MarketService:
    """Service for market operations"""
    
    @staticmethod
    def get_all_markets():
        """Get all markets"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('markets').select('*').execute()
            markets = [Market.from_dict(market) for market in response.data]
            return markets, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_market_by_id(market_id):
        """Get market by ID"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('markets').select('*').eq('id', market_id).execute()
            if response.data:
                return Market.from_dict(response.data[0]), None
            return None, "Market not found"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def create_market(market_data):
        """Create a new market"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('markets').insert(market_data).execute()
            if response.data:
                return Market.from_dict(response.data[0]), None
            return None, "Failed to create market"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def update_market(market_id, market_data):
        """Update a market"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('markets').update(market_data).eq('id', market_id).execute()
            if response.data:
                return Market.from_dict(response.data[0]), None
            return None, "Market not found"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def calculate_market_price(bet_true: float, bet_false: float) -> float:
        """
        Calculate market price based on total bets
        
        Args:
            bet_true: Total amount bet on true
            bet_false: Total amount bet on false
        
        Returns:
            Market price as float between 0.01 and 0.99
        
        Raises:
            ValueError: If bet values are negative
        """
        try:
            bet_true = float(bet_true) if bet_true else 0.0
            bet_false = float(bet_false) if bet_false else 0.0
            
            if bet_true < 0 or bet_false < 0:
                raise ValueError("Bet amounts cannot be negative")
            
            total = bet_true + bet_false
            
            # If both are 0, return 0.50
            if total == 0:
                return 0.50
            
            # Calculate price
            price = bet_true / total
            
            # Clamp to [0.01, 0.99]
            price = max(0.01, min(0.99, price))
            
            return price
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid input for calculate_market_price: {str(e)}")
    
    @staticmethod
    def calculate_shares_for_long(cc: float, price: float) -> float:
        """
        Calculate shares received for a long position (betting true)
        
        Args:
            cc: Collateral cost (amount invested)
            price: Current market price
        
        Returns:
            Number of shares as float
        
        Raises:
            ValueError: If inputs are invalid
        """
        try:
            cc = float(cc)
            price = float(price)
            
            if cc <= 0:
                raise ValueError("Collateral cost must be positive")
            if price <= 0 or price >= 1:
                raise ValueError("Price must be between 0 and 1")
            
            shares = cc / price
            return shares
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid input for calculate_shares_for_long: {str(e)}")
    
    @staticmethod
    def calculate_shares_for_short(cc: float, price: float) -> float:
        """
        Calculate shares received for a short position (betting false)
        
        Args:
            cc: Collateral cost (amount invested)
            price: Current market price
        
        Returns:
            Number of shares as float
        
        Raises:
            ValueError: If inputs are invalid
        """
        try:
            cc = float(cc)
            price = float(price)
            
            if cc <= 0:
                raise ValueError("Collateral cost must be positive")
            if price <= 0 or price >= 1:
                raise ValueError("Price must be between 0 and 1")
            
            shares = cc / (1.0 - price)
            return shares
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid input for calculate_shares_for_short: {str(e)}")
    
    @staticmethod
    def calculate_collateral(shares: float, entry_price: float) -> float:
        """
        Calculate collateral required for a position
        
        Args:
            shares: Number of shares
            entry_price: Entry price of the position
        
        Returns:
            Collateral amount as float
        
        Raises:
            ValueError: If inputs are invalid
        """
        try:
            shares = float(shares)
            entry_price = float(entry_price)
            
            if shares < 0:
                raise ValueError("Shares cannot be negative")
            if entry_price < 0 or entry_price > 1:
                raise ValueError("Entry price must be between 0 and 1")
            
            collateral = shares * (1.0 - entry_price)
            return max(0.0, collateral)  # Ensure non-negative
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid input for calculate_collateral: {str(e)}")
    
    @staticmethod
    def validate_trade(user_id: str, market_id: str, cc: float) -> Dict:
        """
        Validate if a trade can be executed
        
        Args:
            user_id: User ID making the trade
            market_id: Market ID for the trade
            cc: Collateral cost (amount to invest)
        
        Returns:
            Dictionary with 'valid' (bool) and 'error' (str) keys
        
        Raises:
            Exception: For database or unexpected errors
        """
        try:
            cc = float(cc)
            
            # Check cc > 0
            if cc <= 0:
                return {
                    'valid': False,
                    'error': 'Collateral cost must be greater than 0'
                }
            
            # Get user from database
            supabase = get_supabase_client()
            user_response = supabase.table('users').select('*').eq('id', user_id).execute()
            
            if not user_response.data:
                return {
                    'valid': False,
                    'error': 'User not found'
                }
            
            user_data = user_response.data[0]
            user = User.from_dict(user_data)
            
            # Check user balance >= cc
            if user.available_balance < cc:
                return {
                    'valid': False,
                    'error': f'Insufficient balance. Available: {user.available_balance}, Required: {cc}'
                }
            
            # Get market from database
            market_response = supabase.table('markets').select('*').eq('id', market_id).execute()
            
            if not market_response.data:
                return {
                    'valid': False,
                    'error': 'Market not found'
                }
            
            market_data = market_response.data[0]
            market = Market.from_dict(market_data)
            
            # Check market is active
            if not market.is_active():
                return {
                    'valid': False,
                    'error': f'Market is not active. Current status: {market.status}'
                }
            
            # All validations passed
            return {
                'valid': True,
                'error': None
            }
            
        except ValueError as e:
            return {
                'valid': False,
                'error': f'Invalid input: {str(e)}'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Validation error: {str(e)}'
            }


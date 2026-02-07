"""Market model for database operations"""

class Market:
    """Market model representation"""
    
    def __init__(self, id=None, text=None, category=None, submitter_id=None,
                 stake=0.0, price=0.5, total_bet_true=0.0, total_bet_false=0.0,
                 status='active', ai_prediction=None, ai_confidence=None,
                 embedding=None, **kwargs):
        self.id = id
        self.text = text
        self.category = category
        self.submitter_id = submitter_id
        self.stake = float(stake) if stake else 0.0
        self.price = float(price) if price else 0.5
        self.total_bet_true = float(total_bet_true) if total_bet_true else 0.0
        self.total_bet_false = float(total_bet_false) if total_bet_false else 0.0
        self.status = status
        self.ai_prediction = ai_prediction
        self.ai_confidence = float(ai_confidence) if ai_confidence else None
        self.embedding = embedding
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update_price(self):
        """Update market price based on total bets"""
        total = self.total_bet_true + self.total_bet_false
        if total > 0:
            self.price = self.total_bet_true / total
        else:
            self.price = 0.5  # Default to 50/50 if no bets
    
    def apply_trade(self, trade_type, amt):
        """
        Apply a trade to the market
        
        Args:
            trade_type: 'true' or 'false'
            amt: Amount of the trade
        """
        amt = float(amt)
        if trade_type.lower() == 'true':
            self.total_bet_true += amt
        elif trade_type.lower() == 'false':
            self.total_bet_false += amt
        else:
            raise ValueError("trade_type must be 'true' or 'false'")
        
        # Update price after trade
        self.update_price()
    
    def is_active(self):
        """Check if market is active"""
        return self.status == 'active'
    
    def to_dict(self):
        """Convert market to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'submitter_id': self.submitter_id,
            'stake': self.stake,
            'price': self.price,
            'total_bet_true': self.total_bet_true,
            'total_bet_false': self.total_bet_false,
            'status': self.status,
            'ai_prediction': self.ai_prediction,
            'ai_confidence': self.ai_confidence,
            'embedding': self.embedding
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create market from dictionary"""
        return cls(**data)


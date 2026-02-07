"""Position model for database operations"""

class Position:
    """Position model representation"""
    
    def __init__(self, id=None, user_id=None, market_id=None, type=None,
                 shares=0.0, entry_price=0.0, cost_basis=0.0, collateral=0.0,
                 status='open', **kwargs):
        self.id = id
        self.user_id = user_id
        self.market_id = market_id
        self.type = type  # 'true' or 'false'
        self.shares = float(shares) if shares else 0.0
        self.entry_price = float(entry_price) if entry_price else 0.0
        self.cost_basis = float(cost_basis) if cost_basis else 0.0
        self.collateral = float(collateral) if collateral else 0.0
        self.status = status
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calculate_unrealized_pnl(self, current_price):
        """
        Calculate unrealized profit/loss based on current market price
        
        Args:
            current_price: Current market price
        
        Returns:
            Unrealized PnL value
        """
        if self.type == 'true':
            # If betting true, profit when price goes up
            pnl = (current_price - self.entry_price) * self.shares
        elif self.type == 'false':
            # If betting false, profit when price goes down
            pnl = (self.entry_price - current_price) * self.shares
        else:
            raise ValueError("Position type must be 'true' or 'false'")
        
        return pnl
    
    def calculate_payout_if_true(self):
        """
        Calculate payout if market resolves to true
        
        Returns:
            Payout amount
        """
        if self.type == 'true':
            # If you bet true and it's true, you get: shares * (1 / entry_price)
            # This represents the total value of your shares at resolution
            if self.entry_price > 0:
                return self.shares / self.entry_price
            return 0.0
        elif self.type == 'false':
            # If you bet false and it's true, you get nothing
            return 0.0
        else:
            raise ValueError("Position type must be 'true' or 'false'")
    
    def calculate_payout_if_false(self):
        """
        Calculate payout if market resolves to false
        
        Returns:
            Payout amount
        """
        if self.type == 'false':
            # If you bet false and it's false, you get: shares * (1 / (1 - entry_price))
            # This represents the total value of your shares at resolution
            if self.entry_price < 1.0:
                return self.shares / (1 - self.entry_price)
            return 0.0
        elif self.type == 'true':
            # If you bet true and it's false, you get nothing
            return 0.0
        else:
            raise ValueError("Position type must be 'true' or 'false'")
    
    def to_dict(self):
        """Convert position to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'market_id': self.market_id,
            'type': self.type,
            'shares': self.shares,
            'entry_price': self.entry_price,
            'cost_basis': self.cost_basis,
            'collateral': self.collateral,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create position from dictionary"""
        return cls(**data)


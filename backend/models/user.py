"""User model for database operations"""

class User:
    """User model representation"""
    
    def __init__(self, id=None, pseudonym=None, available_balance=0.0, 
                 locked_balance=0.0, total_earned=0.0, total_lost=0.0, **kwargs):
        self.id = id
        self.pseudonym = pseudonym
        self.available_balance = float(available_balance) if available_balance else 0.0
        self.locked_balance = float(locked_balance) if locked_balance else 0.0
        self.total_earned = float(total_earned) if total_earned else 0.0
        self.total_lost = float(total_lost) if total_lost else 0.0
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def lock_balance(self, amt):
        """Lock a specified amount from available balance"""
        amt = float(amt)
        if amt > self.available_balance:
            raise ValueError("Insufficient available balance")
        self.available_balance -= amt
        self.locked_balance += amt
    
    def unlock_balance(self, amt):
        """Unlock a specified amount back to available balance"""
        amt = float(amt)
        if amt > self.locked_balance:
            raise ValueError("Insufficient locked balance")
        self.locked_balance -= amt
        self.available_balance += amt
    
    def add_earnings(self, amt):
        """Add earnings to user's total earned"""
        amt = float(amt)
        self.total_earned += amt
        self.available_balance += amt
    
    def deduct_loss(self, amt):
        """Deduct loss from user's total lost"""
        amt = float(amt)
        self.total_lost += amt
        # Loss is already deducted from available_balance when position is closed
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'pseudonym': self.pseudonym,
            'available_balance': self.available_balance,
            'locked_balance': self.locked_balance,
            'total_earned': self.total_earned,
            'total_lost': self.total_lost
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary"""
        return cls(**data)


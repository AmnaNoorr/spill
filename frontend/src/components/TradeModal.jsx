import React, { useState, useEffect } from 'react';
import { X, TrendingUp, TrendingDown, Info, AlertCircle, Loader2 } from 'lucide-react';
import { marketsAPI } from '../services/api';
import { useAuth } from '../hooks/useAuth';

const TradeModal = ({ market, onClose, onComplete }) => {
    const { user } = useAuth();
    const [position, setPosition] = useState('long'); // 'long' or 'short'
    const [amount, setAmount] = useState(50);
    const [shares, setShares] = useState(0);
    const [potentialReturn, setPotentialReturn] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Get current price from market
    const currentPrice = market.price || 0.5;
    const price = position === 'long' ? currentPrice : 1 - currentPrice;

    useEffect(() => {
        // Calculate estimated shares and return
        if (position === 'long') {
            // Long: shares = amount / price
            const estimatedShares = amount / currentPrice;
            setShares(estimatedShares);
            // If true, payout = shares / entry_price
            setPotentialReturn(estimatedShares / currentPrice);
        } else {
            // Short: shares = amount / (1 - price)
            const estimatedShares = amount / (1 - currentPrice);
            setShares(estimatedShares);
            // If false, payout = shares / (1 - entry_price)
            setPotentialReturn(estimatedShares / (1 - currentPrice));
        }
    }, [amount, position, currentPrice]);

    const handleSubmit = async () => {
        if (!user || !user.id) {
            setError('Please initialize your account first');
            return;
        }

        if (amount <= 0) {
            setError('Amount must be greater than 0');
            return;
        }

        try {
            setLoading(true);
            setError(null);
            
            const response = await marketsAPI.placeBet(market.id, {
                user_id: user.id,
                type: position,
                cc_amount: amount,
            });

            if (response) {
                onComplete();
            }
        } catch (err) {
            setError(err.message || 'Failed to place bet');
        } finally {
            setLoading(false);
        }
    };

    if (!market) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.7)',
            backdropFilter: 'blur(4px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            transition: 'opacity 0.2s'
            }} onClick={onClose}>
            <div className="trade-modal" style={{
                position: 'relative',
                background: 'var(--bg-secondary)',
                width: '100%',
                maxWidth: '480px',
                borderRadius: '16px',
                border: '1px solid var(--border-color)',
                boxShadow: 'var(--shadow-lg)',
                overflow: 'hidden',
                animation: 'slideUp 0.3s ease-out'
            }} onClick={(e) => e.stopPropagation()}>
                {/* Header */}
                <div style={{
                    padding: '20px',
                    borderBottom: '1px solid var(--border-color)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'start'
                }}>
                    <div>
                        <h3 style={{ margin: 0, fontSize: '1.25rem', color: 'var(--text-primary)' }}>Trade Position</h3>
                        <p style={{ margin: '4px 0 0', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                            {market.text || market.title}
                        </p>
                    </div>
                    <button onClick={onClose} style={{
                        background: 'transparent',
                        border: 'none',
                        color: 'var(--text-tertiary)',
                        cursor: 'pointer',
                        padding: '4px'
                    }}>
                        <X size={24} />
                    </button>
                </div>

                {/* Body */}
                <div style={{ padding: '24px' }}>
                    {/* Toggle Switch */}
                    <div style={{
                        background: 'var(--bg-tertiary)',
                        padding: '4px',
                        borderRadius: '12px',
                        display: 'flex',
                        marginBottom: '24px'
                    }}>
                        <button
                            onClick={() => setPosition('long')}
                            style={{
                                flex: 1,
                                padding: '12px',
                                border: 'none',
                                borderRadius: '8px',
                                background: position === 'long' ? 'var(--success)' : 'transparent',
                                color: position === 'long' ? 'white' : 'var(--text-secondary)',
                                fontWeight: 600,
                                cursor: 'pointer',
                                transition: 'all 0.2s'
                            }}
                        >
                            Buy YES ({Math.round(currentPrice * 100)}%)
                        </button>
                        <button
                            onClick={() => setPosition('short')}
                            style={{
                                flex: 1,
                                padding: '12px',
                                border: 'none',
                                borderRadius: '8px',
                                background: position === 'short' ? 'var(--danger)' : 'transparent',
                                color: position === 'short' ? 'white' : 'var(--text-secondary)',
                                fontWeight: 600,
                                cursor: 'pointer',
                                transition: 'all 0.2s'
                            }}
                        >
                            Buy NO ({Math.round((1 - currentPrice) * 100)}%)
                        </button>
                    </div>

                    {/* Stats */}
                    <div style={{
                        display: 'flex',
                        gap: '12px',
                        marginBottom: '24px'
                    }}>
                        <div style={{ flex: 1, padding: '12px', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginBottom: '4px' }}>Current Price</div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                                {Math.round(currentPrice * 100)}%
                            </div>
                        </div>
                        <div style={{ flex: 1, padding: '12px', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginBottom: '4px' }}>Shares</div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--success)' }}>
                                {shares.toFixed(2)}
                            </div>
                        </div>
                    </div>

                    {/* Amount Input */}
                    <div style={{ marginBottom: '24px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, color: 'var(--text-primary)' }}>
                            Amount to Invest (CC)
                        </label>
                        <div style={{ position: 'relative' }}>
                            <input
                                type="number"
                                value={amount}
                                onChange={(e) => setAmount(Number(e.target.value))}
                                style={{
                                    width: '100%',
                                    padding: '16px',
                                    fontSize: '1.2rem',
                                    background: 'var(--bg-tertiary)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: '12px',
                                    color: 'var(--text-primary)',
                                    fontWeight: 600
                                }}
                            />
                            <span style={{
                                position: 'absolute',
                                right: '16px',
                                top: '50%',
                                transform: 'translateY(-50%)',
                                color: 'var(--text-tertiary)',
                                fontWeight: 500
                            }}>CC</span>
                        </div>
                        <div style={{ marginTop: '8px', display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                            <span style={{ color: 'var(--text-tertiary)' }}>
                                Balance: {user?.available_balance?.toFixed(2) || '0'} CC
                            </span>
                            <span 
                                style={{ color: 'var(--accent-primary)', cursor: 'pointer' }} 
                                onClick={() => setAmount(user?.available_balance || 0)}
                            >
                                Max
                            </span>
                        </div>
                        {error && (
                            <div style={{
                                marginTop: '12px',
                                padding: '12px',
                                background: 'rgba(239, 68, 68, 0.1)',
                                border: '1px solid rgba(239, 68, 68, 0.3)',
                                borderRadius: '8px',
                                color: 'var(--danger)',
                                fontSize: '0.9rem'
                            }}>
                                {error}
                            </div>
                        )}
                    </div>

                    {/* Order Summary */}
                    <div style={{
                        padding: '16px',
                        background: 'rgba(59, 130, 246, 0.1)',
                        border: '1px solid rgba(59, 130, 246, 0.2)',
                        borderRadius: '12px',
                        marginBottom: '24px'
                    }}>
                        <div style={{ display: 'flex', gap: '8px', alignItems: 'start', color: 'var(--accent-primary)' }}>
                            <Info size={18} style={{ marginTop: '2px' }} />
                            <p style={{ margin: 0, fontSize: '0.9rem', lineHeight: '1.4' }}>
                                You are buying <strong>{shares.toFixed(2)} shares</strong> of "{position === 'long' ? 'TRUE' : 'FALSE'}" for <strong>{amount} CC</strong>. 
                                If the market validates {position === 'long' ? 'TRUE' : 'FALSE'}, you win <strong>{potentialReturn.toFixed(2)} CC</strong>.
                            </p>
                        </div>
                    </div>

                    {/* Action Button */}
                    <button 
                        onClick={handleSubmit}
                        disabled={loading || !user}
                        style={{
                            width: '100%',
                            padding: '16px',
                            background: position === 'long' ? 'var(--success)' : 'var(--danger)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '12px',
                            fontSize: '1.1rem',
                            fontWeight: 700,
                            cursor: loading || !user ? 'not-allowed' : 'pointer',
                            boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                            transition: 'transform 0.1s',
                            opacity: loading || !user ? 0.6 : 1,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '8px'
                        }}
                    >
                        {loading ? (
                            <>
                                <Loader2 size={20} className="animate-spin" />
                                Placing Order...
                            </>
                        ) : (
                            `Place ${position === 'long' ? 'Buy' : 'Short'} Order`
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default TradeModal;

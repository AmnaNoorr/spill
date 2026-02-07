import React, { useState, useEffect } from 'react';
import { Search, Filter, TrendingUp, Clock, Users, Volume2, Loader2 } from 'lucide-react';
import { marketsAPI } from '../services/api';
import TradeModal from './TradeModal';

const Markets = () => {
    const [filter, setFilter] = useState('all');
    const [markets, setMarkets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedMarket, setSelectedMarket] = useState(null);
    const [showTradeModal, setShowTradeModal] = useState(false);

    useEffect(() => {
        loadMarkets();
    }, [filter]);

    const loadMarkets = async () => {
        try {
            setLoading(true);
            setError(null);
            const params = {
                status: 'active',
                limit: 50,
                offset: 0,
            };
            if (filter !== 'all') {
                params.category = filter.charAt(0).toUpperCase() + filter.slice(1);
            }
            const response = await marketsAPI.getMarkets(params);
            setMarkets(response.markets || []);
        } catch (err) {
            setError(err.message);
            console.error('Error loading markets:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleTrade = (market, type) => {
        setSelectedMarket({ ...market, tradeType: type });
        setShowTradeModal(true);
    };

    const handleTradeComplete = () => {
        setShowTradeModal(false);
        setSelectedMarket(null);
        loadMarkets(); // Reload markets after trade
    };

    const getProbabilityColor = (prob) => {
        if (prob >= 70) return 'var(--success)';
        if (prob >= 40) return 'var(--warning)';
        return 'var(--danger)';
    };

    const formatPrice = (price) => {
        return Math.round(price * 100);
    };

    const formatCurrency = (amount) => {
        if (amount >= 1000) {
            return `${(amount / 1000).toFixed(1)}k CC`;
        }
        return `${amount.toFixed(0)} CC`;
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
                <Loader2 size={32} className="animate-spin" style={{ color: 'var(--accent-primary)' }} />
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ 
                padding: '24px', 
                background: 'var(--bg-secondary)', 
                borderRadius: '12px', 
                border: '1px solid var(--danger)',
                color: 'var(--danger)'
            }}>
                Error loading markets: {error}
                <button 
                    onClick={loadMarkets}
                    style={{
                        marginTop: '16px',
                        padding: '8px 16px',
                        background: 'var(--accent-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer'
                    }}
                >
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="markets-container" style={{ animation: 'slideUp 0.5s ease-out' }}>
            {showTradeModal && selectedMarket && (
                <TradeModal
                    market={selectedMarket}
                    onClose={() => setShowTradeModal(false)}
                    onComplete={handleTradeComplete}
                />
            )}
            <div className="markets-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px', flexWrap: 'wrap', gap: '16px' }}>
                <div>
                    <h2 style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 8px 0' }}>Active Markets</h2>
                    <p style={{ color: 'var(--text-tertiary)', margin: 0, fontSize: '0.9rem' }}>Trade on campus rumors with prediction markets</p>
                </div>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {['All', 'Tech', 'Campus', 'Lifestyle'].map(f => (
                        <button
                            key={f}
                            onClick={() => setFilter(f.toLowerCase())}
                            style={{
                                padding: '8px 16px',
                                background: filter === f.toLowerCase() ? 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))' : 'var(--bg-tertiary)',
                                color: filter === f.toLowerCase() ? 'white' : 'var(--text-secondary)',
                                border: '1px solid var(--border-color)',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                transition: 'all 0.3s',
                                fontWeight: 500,
                                fontSize: '0.9rem'
                            }}
                        >
                            {f}
                        </button>
                    ))}
                </div>
            </div>

            <div className="markets-grid" style={{ display: 'grid', gap: '20px', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))' }}>
                {markets.map(market => (
                    <div key={market.id} className="market-card" style={{
                        background: 'var(--bg-secondary)',
                        border: '1px solid var(--border-color)',
                        borderRadius: '12px',
                        padding: '24px',
                        transition: 'transform 0.3s, box-shadow 0.3s, border-color 0.3s',
                        cursor: 'pointer',
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column'
                    }} onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-4px)';
                        e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
                        e.currentTarget.style.borderColor = 'var(--accent-primary)';
                    }} onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = 'none';
                        e.currentTarget.style.borderColor = 'var(--border-color)';
                    }}>
                        <div className="market-card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px', gap: '12px' }}>
                            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', flex: 1, lineHeight: 1.4 }}>{market.text || market.title}</h3>
                            <div style={{
                                background: getProbabilityColor(formatPrice(market.price || 0.5)),
                                color: 'white',
                                padding: '8px 12px',
                                borderRadius: '8px',
                                fontWeight: 700,
                                fontSize: '1rem',
                                whiteSpace: 'nowrap'
                            }}>
                                {formatPrice(market.price || 0.5)}%
                            </div>
                        </div>

                        <div className="market-meta" style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(2, 1fr)',
                            gap: '12px',
                            padding: '16px',
                            background: 'var(--bg-tertiary)',
                            borderRadius: '8px',
                            marginBottom: '20px',
                            flex: 1
                        }}>
                            <div>
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '4px' }}>Volume</div>
                                <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.95rem' }}>
                                    {formatCurrency((market.total_bet_true || 0) + (market.total_bet_false || 0))}
                                </div>
                            </div>
                            <div>
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '4px' }}>Liquidity</div>
                                <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.95rem' }}>
                                    {formatCurrency((market.total_bet_true || 0) + (market.total_bet_false || 0))}
                                </div>
                            </div>
                            <div>
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '4px' }}>Expires</div>
                                <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.95rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
                                    <Clock size={14} />
                                    {market.expires}
                                </div>
                            </div>
                            <div>
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '4px' }}>Traders</div>
                                <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.95rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
                                    <Users size={14} />
                                    {market.positions_count || 0}
                                </div>
                            </div>
                        </div>

                        <div className="trading-section" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginTop: 'auto' }}>
                            <button 
                                onClick={() => handleTrade(market, 'long')}
                                style={{
                                    padding: '12px 16px',
                                    border: 'none',
                                    borderRadius: '8px',
                                    fontWeight: 600,
                                    cursor: 'pointer',
                                    background: 'var(--success)',
                                    color: 'white',
                                    transition: 'all 0.3s',
                                    fontSize: '0.95rem'
                                }} 
                                onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'} 
                                onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
                            >
                                Yes
                            </button>
                            <button 
                                onClick={() => handleTrade(market, 'short')}
                                style={{
                                    padding: '12px 16px',
                                    border: 'none',
                                    borderRadius: '8px',
                                    fontWeight: 600,
                                    cursor: 'pointer',
                                    background: 'var(--danger)',
                                    color: 'white',
                                    transition: 'all 0.3s',
                                    fontSize: '0.95rem'
                                }} 
                                onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'} 
                                onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
                            >
                                No
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Markets;

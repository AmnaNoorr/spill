import React from 'react';
import { X, TrendingUp, DollarSign, PieChart, Award } from 'lucide-react';

const PortfolioSidebar = ({ isOpen, onClose }) => {
    return (
        <>
            {/* Overlay */}
            <div
                onClick={onClose}
                style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    background: 'rgba(0,0,0,0.5)',
                    zIndex: 998,
                    opacity: isOpen ? 1 : 0,
                    visibility: isOpen ? 'visible' : 'hidden',
                    transition: 'opacity 0.3s, visibility 0.3s',
                    backdropFilter: 'blur(2px)'
                }}></div>

            {/* Sidebar */}
            <div style={{
                position: 'fixed',
                top: 0,
                right: 0,
                height: '100vh',
                width: '390px',
                background: 'var(--bg-secondary)',
                boxShadow: '-5px 0 30px rgba(0,0,0,0.2)',
                zIndex: 999,
                transform: isOpen ? 'translateX(0)' : 'translateX(100%)',
                transition: 'transform 0.3s ease-in-out',
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden'
            }}>
                {/* Header */}
                <div style={{
                    padding: '24px',
                    borderBottom: '1px solid var(--border-color)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    background: 'var(--bg-tertiary)'
                }}>
                    <h2 style={{ fontSize: '1.4rem', fontWeight: 700, margin: 0, color: 'var(--text-primary)' }}>My Portfolio</h2>
                    <button onClick={onClose} style={{
                        width: '36px',
                        height: '36px',
                        background: 'var(--bg-secondary)',
                        border: '1px solid var(--border-color)',
                        cursor: 'pointer',
                        color: 'var(--text-secondary)',
                        borderRadius: '6px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        transition: 'all 0.3s'
                    }} onMouseEnter={(e) => {
                        e.target.style.background = 'var(--border-color)';
                        e.target.style.color = 'var(--text-primary)';
                    }} onMouseLeave={(e) => {
                        e.target.style.background = 'var(--bg-secondary)';
                        e.target.style.color = 'var(--text-secondary)';
                    }}>
                        <X size={20} />
                    </button>
                </div>

                {/* Content */}
                <div style={{ flex: 1, overflowY: 'auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    {/* Stats */}
                    <div style={{
                        background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
                        borderRadius: '12px',
                        padding: '24px',
                        color: 'white',
                        boxShadow: 'var(--shadow-md)',
                        border: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                        <div style={{ fontSize: '0.8rem', opacity: 0.9, textTransform: 'uppercase', fontWeight: 600, marginBottom: '8px' }}>Total PnL</div>
                        <div style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '16px' }}>+24.5%</div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                            <div>
                                <div style={{ fontSize: '0.75rem', opacity: 0.8, marginBottom: '4px' }}>INVESTED</div>
                                <div style={{ fontWeight: 700, fontSize: '1.25rem' }}>450 CC</div>
                            </div>
                            <div>
                                <div style={{ fontSize: '0.75rem', opacity: 0.8, marginBottom: '4px' }}>AVAILABLE</div>
                                <div style={{ fontWeight: 700, fontSize: '1.25rem' }}>550 CC</div>
                            </div>
                        </div>
                    </div>

                    {/* Performance Metrics */}
                    <div style={{
                        background: 'var(--bg-tertiary)',
                        borderRadius: '12px',
                        padding: '16px',
                        border: '1px solid var(--border-color)'
                    }}>
                        <h4 style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '12px', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Award size={16} />
                            Performance
                        </h4>
                        <div style={{ display: 'grid', gap: '10px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.9rem' }}>
                                <span style={{ color: 'var(--text-secondary)' }}>Win Rate</span>
                                <span style={{ fontWeight: 600, color: 'var(--success)' }}>65%</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.9rem' }}>
                                <span style={{ color: 'var(--text-secondary)' }}>Total Trades</span>
                                <span style={{ fontWeight: 600 }}>42</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.9rem' }}>
                                <span style={{ color: 'var(--text-secondary)' }}>Markets Won</span>
                                <span style={{ fontWeight: 600, color: 'var(--success)' }}>27</span>
                            </div>
                        </div>
                    </div>

                    <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '12px', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <TrendingUp size={18} />
                        Active Positions
                    </h3>

                    <div className="position-list" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        {[1, 2].map(i => (
                            <div key={i} style={{
                                background: 'var(--bg-tertiary)',
                                borderRadius: '8px',
                                padding: '16px',
                                border: '1px solid var(--border-color)',
                                transition: 'all 0.3s'
                            }} onMouseEnter={(e) => {
                                e.currentTarget.style.borderColor = 'var(--accent-primary)';
                                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                            }} onMouseLeave={(e) => {
                                e.currentTarget.style.borderColor = 'var(--border-color)';
                                e.currentTarget.style.boxShadow = 'none';
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px', alignItems: 'start' }}>
                                    <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-primary)', flex: 1 }}>
                                        {i === 1 ? 'Project Orion Cancelled?' : 'Dean Resigning?'}
                                    </span>
                                    <span style={{
                                        background: i === 1 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                                        color: i === 1 ? 'var(--success)' : 'var(--danger)',
                                        padding: '4px 10px',
                                        borderRadius: '4px',
                                        fontSize: '0.75rem',
                                        fontWeight: 700,
                                        whiteSpace: 'nowrap',
                                        marginLeft: '8px'
                                    }}>{i === 1 ? 'YES' : 'NO'}</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-tertiary)', marginBottom: '8px' }}>
                                    <span>100 Shares @ 0.45</span>
                                    <span style={{ color: i === 1 ? 'var(--success)' : 'var(--danger)', fontWeight: 600 }}>
                                        {i === 1 ? '+12 CC' : '-5 CC'}
                                    </span>
                                </div>
                                <div style={{
                                    background: 'var(--bg-secondary)',
                                    borderRadius: '4px',
                                    height: '4px',
                                    overflow: 'hidden'
                                }}>
                                    <div style={{
                                        height: '100%',
                                        width: i === 1 ? '70%' : '45%',
                                        background: i === 1 ? 'var(--success)' : 'var(--danger)',
                                        transition: 'width 0.3s'
                                    }}></div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Empty State Info */}
                    <div style={{
                        marginTop: 'auto',
                        padding: '16px',
                        background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(16, 185, 129, 0.1))',
                        borderRadius: '8px',
                        fontSize: '0.85rem',
                        color: 'var(--text-secondary)',
                        textAlign: 'center',
                        borderLeft: '3px solid var(--accent-primary)'
                    }}>
                        <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>💡 Tip</div>
                        <div>Diversify across markets to minimize risk and maximize long-term returns.</div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default PortfolioSidebar;

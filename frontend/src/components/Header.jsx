import React from 'react';
import { User, Sun, Moon } from 'lucide-react';

const Header = ({ theme, toggleTheme, onOpenPortfolio, user }) => {
    const balance = user?.available_balance || 0;
    const pseudonym = user?.pseudonym || 'Guest';
    
    return (
        <header style={{
            position: 'sticky',
            top: 0,
            background: 'var(--bg-secondary)',
            borderBottom: '1px solid var(--border-color)',
            zIndex: 100,
            backdropFilter: 'blur(10px)',
            boxShadow: 'var(--shadow-sm)'
        }}>
            <div style={{
                maxWidth: '1400px',
                margin: '0 auto',
                padding: '0 24px',
                height: '70px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
            }}>
                {/* Logo */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer', transition: 'transform 0.2s' }} onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.02)'} onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
                    <div style={{ fontSize: '1.8rem', animation: 'float 3s ease-in-out infinite' }}>☕</div>
                    <div>
                        <h1 style={{ fontFamily: "'Playfair Display', 'Georgia', serif", fontSize: '1.4rem', color: 'var(--accent-primary)', fontWeight: 700, margin: 0, letterSpacing: '-0.5px' }}>SipsNSecrets</h1>
                        <p style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', margin: 0, fontWeight: 500 }}>De-Centralized Truth</p>
                    </div>
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    {/* Balance Badge */}
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        background: 'var(--bg-tertiary)',
                        padding: '10px 18px',
                        borderRadius: '50px',
                        border: '1px solid var(--border-color)',
                        transition: 'all 0.3s'
                    }}>
                        <span>💰</span>
                        <span style={{ fontWeight: 600, color: 'var(--accent-primary)', fontSize: '0.95rem' }}>
                            {balance.toFixed(2)} CC
                        </span>
                    </div>
                    
                    {/* User Pseudonym */}
                    {user && (
                        <div style={{
                            padding: '8px 16px',
                            background: 'var(--bg-tertiary)',
                            borderRadius: '20px',
                            border: '1px solid var(--border-color)',
                            fontSize: '0.9rem',
                            color: 'var(--text-secondary)'
                        }}>
                            {pseudonym}
                        </div>
                    )}

                    {/* Theme Toggle */}
                    <button onClick={toggleTheme} style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '8px',
                        background: 'var(--bg-tertiary)',
                        border: '1px solid var(--border-color)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        color: 'var(--text-primary)',
                        transition: 'all 0.3s'
                    }} title={theme === 'light' ? 'Switch to Dark' : 'Switch to Light'}>
                        {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
                    </button>

                    {/* Portfolio Toggle */}
                    <button onClick={onOpenPortfolio} style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '8px',
                        background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
                        border: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        color: 'white',
                        boxShadow: 'var(--shadow-md)',
                        transition: 'transform 0.2s'
                    }} onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'} onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
                        <User size={20} />
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Header;

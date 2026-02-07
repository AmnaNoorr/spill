import React, { useState, useEffect } from 'react';
import SplashScreen from './components/SplashScreen';
import Header from './components/Header';
import PortfolioSidebar from './components/PortfolioSidebar';
import Markets from './components/Markets';
import Submit from './components/Submit';
import Oracle from './components/Oracle';
import { BarChart3, Send, Eye } from 'lucide-react';
import { useAuth } from './hooks/useAuth';
import './styles/global.css';

function App() {
    const { user, loading: authLoading, initialize } = useAuth();
    const [splashComplete, setSplashComplete] = useState(false);
    const [theme, setTheme] = useState('light');
    const [isPortfolioOpen, setIsPortfolioOpen] = useState(false);
    const [currentView, setCurrentView] = useState('markets');
    const [showAuthModal, setShowAuthModal] = useState(false);
    const [pseudonym, setPseudonym] = useState('');
    const [authError, setAuthError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Show auth modal if user is not initialized
    useEffect(() => {
        if (!authLoading && !user) {
            setShowAuthModal(true);
        }
    }, [authLoading, user]);

    const handleAuthSubmit = async (e) => {
        e.preventDefault();
        if (pseudonym.trim()) {
            setIsSubmitting(true);
            setAuthError('');
            try {
                await initialize(pseudonym.trim());
                setShowAuthModal(false);
                setPseudonym('');
            } catch (error) {
                const errorMsg = error.message || 'Failed to initialize user. Please try again.';
                setAuthError(errorMsg);
                console.error('Failed to initialize user:', error);
            } finally {
                setIsSubmitting(false);
            }
        }
    };

    useEffect(() => {
        // Apply theme to body
        document.body.setAttribute('data-theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    const renderView = () => {
        switch (currentView) {
            case 'markets': return <Markets />;
            case 'submit': return <Submit />;
            case 'oracle': return <Oracle />;
            default: return <Markets />;
        }
    };

    return (
        <>
            <SplashScreen onComplete={() => setSplashComplete(true)} />

            {showAuthModal && (
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
                    zIndex: 10000
                }}>
                    <div style={{
                        background: 'var(--bg-secondary)',
                        padding: '32px',
                        borderRadius: '16px',
                        maxWidth: '400px',
                        width: '90%',
                        border: '1px solid var(--border-color)'
                    }}>
                        <h2 style={{ marginTop: 0, marginBottom: '16px', color: 'var(--text-primary)' }}>
                            Enter Your Pseudonym
                        </h2>
                        <p style={{ color: 'var(--text-secondary)', marginBottom: '24px', fontSize: '0.9rem' }}>
                            Choose a pseudonym to start trading. New users receive 100 CC to get started!
                        </p>
                        <form onSubmit={handleAuthSubmit}>
                            <input
                                type="text"
                                value={pseudonym}
                                onChange={(e) => setPseudonym(e.target.value)}
                                placeholder="Your pseudonym"
                                disabled={isSubmitting}
                                style={{
                                    width: '100%',
                                    padding: '12px 16px',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: '8px',
                                    background: 'var(--bg-tertiary)',
                                    color: 'var(--text-primary)',
                                    fontSize: '1rem',
                                    marginBottom: '16px',
                                    opacity: isSubmitting ? 0.6 : 1,
                                    cursor: isSubmitting ? 'not-allowed' : 'auto'
                                }}
                                required
                            />
                            {authError && (
                                <div style={{
                                    background: 'rgba(220, 38, 38, 0.1)',
                                    border: '1px solid rgba(220, 38, 38, 0.3)',
                                    color: '#dc2626',
                                    padding: '12px',
                                    borderRadius: '6px',
                                    marginBottom: '16px',
                                    fontSize: '0.9rem'
                                }}>
                                    {authError}
                                </div>
                            )}
                            <button
                                type="submit"
                                disabled={isSubmitting}
                                style={{
                                    width: '100%',
                                    padding: '12px 16px',
                                    background: isSubmitting ? 'rgba(0, 0, 0, 0.3)' : 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '8px',
                                    fontWeight: 600,
                                    cursor: isSubmitting ? 'not-allowed' : 'pointer',
                                    fontSize: '1rem'
                                }}
                            >
                                {isSubmitting ? 'Creating Profile...' : 'Start Trading'}
                            </button>
                        </form>
                    </div>
                </div>
            )}

            {splashComplete && (
                <div className="app-container" style={{ animation: 'fadeIn 0.6s ease-in' }}>
                    <Header
                        theme={theme}
                        toggleTheme={toggleTheme}
                        onOpenPortfolio={() => setIsPortfolioOpen(true)}
                        user={user}
                    />

                    <PortfolioSidebar
                        isOpen={isPortfolioOpen}
                        onClose={() => setIsPortfolioOpen(false)}
                    />

                    <main className="main-container" style={{ maxWidth: '1400px', margin: '0 auto', padding: '32px 24px' }}>
                        {/* Navigation Tabs */}
                        <div className="nav-tabs" style={{
                            background: 'var(--bg-secondary)',
                            borderRadius: '12px',
                            padding: '8px',
                            display: 'flex',
                            gap: '8px',
                            boxShadow: 'var(--shadow-sm)',
                            marginBottom: '40px',
                            border: '1px solid var(--border-color)'
                        }}>
                            {[
                                { id: 'markets', label: 'Markets', icon: <BarChart3 size={18} /> },
                                { id: 'submit', label: 'Submit Rumor', icon: <Send size={18} /> },
                                { id: 'oracle', label: 'Oracle', icon: <Eye size={18} /> }
                            ].map(tab => (
                                <button
                                    key={tab.id}
                                    onClick={() => setCurrentView(tab.id)}
                                    style={{
                                        flex: 1,
                                        padding: '14px 20px',
                                        background: currentView === tab.id ? 'linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)' : 'transparent',
                                        color: currentView === tab.id ? 'white' : 'var(--text-secondary)',
                                        border: 'none',
                                        borderRadius: '8px',
                                        fontSize: '0.95rem',
                                        fontWeight: 600,
                                        cursor: 'pointer',
                                        transition: 'all 0.3s ease',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '10px',
                                        boxShadow: currentView === tab.id ? 'var(--shadow-md)' : 'none'
                                    }}
                                    onMouseEnter={(e) => {
                                        if (currentView !== tab.id) {
                                            e.currentTarget.style.background = 'var(--bg-tertiary)';
                                        }
                                    }}
                                    onMouseLeave={(e) => {
                                        if (currentView !== tab.id) {
                                            e.currentTarget.style.background = 'transparent';
                                        }
                                    }}
                                >
                                    {tab.icon}
                                    {tab.label}
                                </button>
                            ))}
                        </div>

                        <div className="view-container">
                            {renderView()}
                        </div>
                    </main>
                </div>
            )}
        </>
    );
}

export default App;

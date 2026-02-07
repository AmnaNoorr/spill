import React, { useState } from 'react';
import { Send, AlertCircle, Zap, Loader2 } from 'lucide-react';
import { marketsAPI } from '../services/api';
import { useAuth } from '../hooks/useAuth';

const Submit = () => {
    const { user, initialize } = useAuth();
    const [text, setText] = useState('');
    const [category, setCategory] = useState('');
    const [stake, setStake] = useState(50);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!user || !user.id) {
            setError('Please initialize your account first');
            return;
        }

        if (!text.trim()) {
            setError('Rumor statement is required');
            return;
        }

        if (!category) {
            setError('Category is required');
            return;
        }

        if (stake < 10) {
            setError('Stake must be at least 10 CC');
            return;
        }

        try {
            setLoading(true);
            setError(null);
            setSuccess(false);

            const response = await marketsAPI.submitMarket({
                user_id: user.id,
                text: text.trim(),
                category: category,
                stake: stake,
            });

            if (response.market) {
                setSuccess(true);
                setText('');
                setCategory('');
                setStake(50);
                setTimeout(() => setSuccess(false), 5000);
            }
        } catch (err) {
            setError(err.message || 'Failed to submit market');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="submit-container" style={{ maxWidth: '700px', margin: '0 auto', animation: 'slideUp 0.5s ease-out' }}>
            <div className="submit-card" style={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-color)',
                borderRadius: '12px',
                padding: '40px',
                boxShadow: 'var(--shadow-md)'
            }}>
                <h2 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '12px', color: 'var(--text-primary)' }}>Submit a Rumor</h2>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '32px', fontSize: '0.95rem', lineHeight: 1.6 }}>
                    Create a new prediction market on a verifiable rumor. Your initial stake (50 CC) will be returned if the market resolves.
                </p>

                {success && (
                    <div style={{
                        padding: '16px',
                        background: 'rgba(34, 197, 94, 0.1)',
                        border: '1px solid rgba(34, 197, 94, 0.3)',
                        borderRadius: '8px',
                        color: 'var(--success)',
                        marginBottom: '24px'
                    }}>
                        Market submitted successfully!
                    </div>
                )}

                {error && (
                    <div style={{
                        padding: '16px',
                        background: 'rgba(239, 68, 68, 0.1)',
                        border: '1px solid rgba(239, 68, 68, 0.3)',
                        borderRadius: '8px',
                        color: 'var(--danger)',
                        marginBottom: '24px'
                    }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    <div className="form-group">
                        <label style={{ display: 'block', fontWeight: 600, marginBottom: '10px', color: 'var(--text-primary)', fontSize: '0.95rem' }}>
                            Rumor Statement
                            <span style={{ color: 'var(--danger)', marginLeft: '4px' }}>*</span>
                        </label>
                        <textarea
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="e.g., 'Will the new library open before finals week?'"
                            style={{
                                width: '100%',
                                padding: '14px 16px',
                                border: '1px solid var(--border-color)',
                                borderRadius: '8px',
                                background: 'var(--bg-tertiary)',
                                color: 'var(--text-primary)',
                                minHeight: '120px',
                                fontFamily: 'inherit',
                                resize: 'vertical',
                                fontSize: '0.95rem',
                                lineHeight: 1.5
                            }}
                            required
                        />
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginTop: '6px' }}>Be clear and specific. Avoid ambiguous claims.</p>
                    </div>

                    <div className="form-group">
                        <label style={{ display: 'block', fontWeight: 600, marginBottom: '10px', color: 'var(--text-primary)', fontSize: '0.95rem' }}>
                            Category
                            <span style={{ color: 'var(--danger)', marginLeft: '4px' }}>*</span>
                        </label>
                        <select 
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '14px 16px',
                                border: '1px solid var(--border-color)',
                                borderRadius: '8px',
                                background: 'var(--bg-tertiary)',
                                color: 'var(--text-primary)',
                                fontFamily: 'inherit',
                                fontSize: '0.95rem',
                                cursor: 'pointer'
                            }}
                            required
                        >
                            <option value="">Select a category...</option>
                            <option value="Campus">Campus Life</option>
                            <option value="Tech">Tech & Innovation</option>
                            <option value="Events">Local Events</option>
                            <option value="Academics">Academics & Courses</option>
                            <option value="Lifestyle">Lifestyle</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label style={{ display: 'block', fontWeight: 600, marginBottom: '10px', color: 'var(--text-primary)', fontSize: '0.95rem' }}>
                            Initial Stake (CC)
                            <span style={{ color: 'var(--danger)', marginLeft: '4px' }}>*</span>
                        </label>
                        <input
                            type="number"
                            value={stake}
                            onChange={(e) => setStake(Number(e.target.value))}
                            min="10"
                            step="1"
                            style={{
                                width: '100%',
                                padding: '14px 16px',
                                border: '1px solid var(--border-color)',
                                borderRadius: '8px',
                                background: 'var(--bg-tertiary)',
                                color: 'var(--text-primary)',
                                fontFamily: 'inherit',
                                fontSize: '0.95rem'
                            }}
                            required
                        />
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginTop: '6px' }}>
                            Minimum: 10 CC. Your balance: {user?.available_balance?.toFixed(2) || '0'} CC
                        </p>
                    </div>


                    <div className="term-info" style={{
                        background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05))',
                        borderLeft: '4px solid var(--warning)',
                        padding: '16px',
                        borderRadius: '8px',
                        fontSize: '0.9rem',
                        color: 'var(--text-secondary)',
                        display: 'flex',
                        alignItems: 'start',
                        gap: '12px'
                    }}>
                        <Zap size={18} style={{ minWidth: '18px', marginTop: '2px', color: 'var(--warning)' }} />
                        <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>Market Duration</div>
                            <div>Markets typically resolve within 30 days or upon reaching oracle consensus.</div>
                        </div>
                    </div>

                    <button 
                        type="submit"
                        disabled={loading || !user}
                        style={{
                            width: '100%',
                            padding: '14px 16px',
                            background: loading || !user ? 'var(--bg-tertiary)' : 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
                            color: loading || !user ? 'var(--text-tertiary)' : 'white',
                            border: 'none',
                            borderRadius: '8px',
                            fontWeight: 600,
                            fontSize: '1rem',
                            cursor: loading || !user ? 'not-allowed' : 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '10px',
                            transition: 'transform 0.2s, box-shadow 0.2s',
                            marginTop: '12px',
                            opacity: loading || !user ? 0.6 : 1
                        }} 
                        onMouseEnter={(e) => {
                            if (!loading && user) {
                                e.target.style.transform = 'translateY(-2px)';
                                e.target.style.boxShadow = 'var(--shadow-lg)';
                            }
                        }} 
                        onMouseLeave={(e) => {
                            e.target.style.transform = 'translateY(0)';
                            e.target.style.boxShadow = 'var(--shadow-md)';
                        }}
                    >
                        {loading ? (
                            <>
                                <Loader2 size={18} className="animate-spin" />
                                Submitting...
                            </>
                        ) : (
                            <>
                                <Send size={18} />
                                Submit Rumor
                            </>
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Submit;

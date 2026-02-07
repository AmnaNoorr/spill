import React, { useState, useEffect } from 'react';
import { Eye, CheckCircle, XCircle, Award, TrendingUp, Loader2, AlertCircle, FileText } from 'lucide-react';
import { oracleAPI, marketsAPI } from '../services/api';
import { useAuth } from '../hooks/useAuth';

const Oracle = () => {
    const { user } = useAuth();
    const [oracleStats, setOracleStats] = useState(null);
    const [pendingMarkets, setPendingMarkets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [submittingReport, setSubmittingReport] = useState(null);
    const [showReportModal, setShowReportModal] = useState(null);
    const [reportData, setReportData] = useState({ verdict: '', evidence: [''] });

    useEffect(() => {
        loadOracleData();
    }, [user]);

    const loadOracleData = async () => {
        if (!user || !user.id) {
            setLoading(false);
            return;
        }

        try {
            setLoading(true);
            setError(null);

            // Load oracle reputation stats
            try {
                const stats = await oracleAPI.getOracleReputation(user.id);
                if (stats.oracle) {
                    setOracleStats(stats.oracle);
                } else {
                    // Default stats for new oracles
                    setOracleStats({
                        reputation: 50.0,
                        total_reports: 0,
                        correct_count: 0,
                        incorrect_count: 0,
                        accuracy: 0.0
                    });
                }
            } catch (err) {
                console.warn('Could not load oracle stats:', err);
                setOracleStats({
                    reputation: 50.0,
                    total_reports: 0,
                    correct_count: 0,
                    incorrect_count: 0,
                    accuracy: 0.0
                });
            }

            // Load active markets that need resolution
            const marketsResponse = await marketsAPI.getMarkets({ status: 'active', limit: 20 });
            setPendingMarkets(marketsResponse.markets || []);

        } catch (err) {
            setError(err.message);
            console.error('Error loading oracle data:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmitReport = async (marketId) => {
        if (!user || !user.id) {
            setError('Please initialize your account first');
            return;
        }

        if (!reportData.verdict) {
            setError('Please select a verdict (True or False)');
            return;
        }

        try {
            setSubmittingReport(marketId);
            setError(null);

            // Filter out empty evidence URLs
            const evidence = reportData.evidence.filter(url => url.trim() !== '');

            await oracleAPI.submitReport({
                oracle_id: user.id,
                market_id: marketId,
                verdict: reportData.verdict,
                evidence: evidence,
                stake: 0
            });

            // Reset form and reload data
            setShowReportModal(null);
            setReportData({ verdict: '', evidence: [''] });
            await loadOracleData();
        } catch (err) {
            setError(err.message || 'Failed to submit report');
            console.error('Error submitting report:', err);
        } finally {
            setSubmittingReport(null);
        }
    };

    const addEvidenceField = () => {
        setReportData({
            ...reportData,
            evidence: [...reportData.evidence, '']
        });
    };

    const updateEvidence = (index, value) => {
        const newEvidence = [...reportData.evidence];
        newEvidence[index] = value;
        setReportData({ ...reportData, evidence: newEvidence });
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
                <Loader2 size={32} className="animate-spin" style={{ color: 'var(--accent-primary)' }} />
            </div>
        );
    }

    if (!user || !user.id) {
        return (
            <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '40px', textAlign: 'center' }}>
                <Eye size={64} style={{ marginBottom: '24px', opacity: 0.5, color: 'var(--text-tertiary)' }} />
                <h2 style={{ marginBottom: '16px', color: 'var(--text-primary)' }}>Oracle Dashboard</h2>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                    Please initialize your account to access the Oracle Dashboard and submit truth reports.
                </p>
            </div>
        );
    }

    return (
        <div className="oracle-container" style={{ maxWidth: '1000px', margin: '0 auto', animation: 'slideUp 0.5s ease-out' }}>
            {/* Hero Section */}
            <div style={{
                background: 'linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)',
                color: 'white',
                borderRadius: '12px',
                padding: '40px',
                marginBottom: '32px',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div style={{
                    position: 'absolute',
                    top: '-50%',
                    right: '-10%',
                    width: '400px',
                    height: '400px',
                    background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%)',
                    borderRadius: '50%',
                    pointerEvents: 'none'
                }}></div>
                <div style={{ position: 'relative', zIndex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '12px' }}>
                        <Eye size={32} />
                        <h2 style={{ fontSize: '2rem', marginBottom: 0, fontWeight: 700 }}>Oracle Dashboard</h2>
                    </div>
                    <p style={{ opacity: 0.95, lineHeight: 1.6, fontSize: '1.05rem', marginBottom: '24px' }}>
                        Help resolve markets by providing evidence-based truth reports. Your reliability increases your verification power and rewards.
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px' }}>
                        <div style={{ background: 'rgba(255,255,255,0.15)', padding: '20px', borderRadius: '8px', backdropFilter: 'blur(10px)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                                <Award size={20} />
                                <div style={{ fontSize: '0.8rem', opacity: 0.9, fontWeight: 600 }}>Reputation</div>
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 700 }}>
                                {oracleStats ? `${Math.round(oracleStats.reputation)}%` : '50%'}
                            </div>
                        </div>
                        <div style={{ background: 'rgba(255,255,255,0.15)', padding: '20px', borderRadius: '8px', backdropFilter: 'blur(10px)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                                <CheckCircle size={20} />
                                <div style={{ fontSize: '0.8rem', opacity: 0.9, fontWeight: 600 }}>Reports</div>
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 700 }}>
                                {oracleStats ? oracleStats.total_reports : '0'}
                            </div>
                        </div>
                        <div style={{ background: 'rgba(255,255,255,0.15)', padding: '20px', borderRadius: '8px', backdropFilter: 'blur(10px)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                                <TrendingUp size={20} />
                                <div style={{ fontSize: '0.8rem', opacity: 0.9, fontWeight: 600 }}>Accuracy</div>
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 700 }}>
                                {oracleStats ? `${Math.round(oracleStats.accuracy)}%` : '0%'}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div style={{
                    marginBottom: '24px',
                    padding: '16px',
                    background: 'var(--danger)',
                    color: 'white',
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px'
                }}>
                    <AlertCircle size={20} />
                    <div>{error}</div>
                </div>
            )}

            {/* Markets to Resolve */}
            <div className="markets-to-resolve" style={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-color)',
                borderRadius: '12px',
                padding: '32px',
                overflow: 'hidden'
            }}>
                <h3 style={{ marginBottom: '24px', fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    Markets Pending Resolution ({pendingMarkets.length})
                </h3>
                {pendingMarkets.length === 0 ? (
                    <div style={{
                        padding: '40px',
                        textAlign: 'center',
                        color: 'var(--text-tertiary)'
                    }}>
                        <Eye size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
                        <div>No active markets need resolution at the moment.</div>
                    </div>
                ) : (
                    <div style={{ display: 'grid', gap: '16px' }}>
                        {pendingMarkets.map((market) => (
                            <div key={market.id} style={{
                                padding: '20px',
                                background: 'var(--bg-tertiary)',
                                borderRadius: '8px',
                                border: '1px solid var(--border-color)',
                                transition: 'all 0.3s'
                            }} onMouseEnter={(e) => {
                                e.currentTarget.style.borderColor = 'var(--accent-primary)';
                                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                            }} onMouseLeave={(e) => {
                                e.currentTarget.style.borderColor = 'var(--border-color)';
                                e.currentTarget.style.boxShadow = 'none';
                            }}>
                                <div style={{ marginBottom: '12px' }}>
                                    <h4 style={{ marginBottom: '8px', fontWeight: 600, color: 'var(--text-primary)', fontSize: '1rem' }}>
                                        {market.text}
                                    </h4>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)', marginBottom: '8px' }}>
                                        Market ID: {market.id.substring(0, 8)}... • Price: {(market.price * 100).toFixed(1)}% • Category: {market.category || 'General'}
                                    </div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)' }}>
                                        True: {market.total_bet_true.toFixed(2)} CC • False: {market.total_bet_false.toFixed(2)} CC
                                    </div>
                                </div>

                                <button
                                    onClick={() => setShowReportModal(market.id)}
                                    style={{
                                        width: '100%',
                                        padding: '12px 16px',
                                        background: 'var(--accent-primary)',
                                        border: 'none',
                                        borderRadius: '6px',
                                        color: 'white',
                                        cursor: 'pointer',
                                        fontWeight: 600,
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '8px',
                                        transition: 'all 0.3s',
                                        fontSize: '0.95rem',
                                        marginTop: '12px'
                                    }}
                                    onMouseEnter={(e) => {
                                        e.target.style.transform = 'translateY(-2px)';
                                        e.target.style.boxShadow = '0 4px 12px rgba(122, 74, 46, 0.2)';
                                    }}
                                    onMouseLeave={(e) => {
                                        e.target.style.transform = 'translateY(0)';
                                        e.target.style.boxShadow = 'none';
                                    }}
                                >
                                    <FileText size={16} />
                                    Submit Oracle Report
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Report Submission Modal */}
            {showReportModal && (
                <div style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(0, 0, 0, 0.7)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 1000,
                    padding: '20px'
                }} onClick={() => {
                    setShowReportModal(null);
                    setReportData({ verdict: '', evidence: [''] });
                }}>
                    <div style={{
                        background: 'var(--bg-primary)',
                        borderRadius: '12px',
                        padding: '32px',
                        maxWidth: '600px',
                        width: '100%',
                        maxHeight: '90vh',
                        overflow: 'auto',
                        border: '1px solid var(--border-color)'
                    }} onClick={(e) => e.stopPropagation()}>
                        <h3 style={{ marginBottom: '24px', fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                            Submit Oracle Report
                        </h3>

                        <div style={{ marginBottom: '20px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontWeight: 600, color: 'var(--text-primary)' }}>
                                Verdict *
                            </label>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                                <button
                                    onClick={() => setReportData({ ...reportData, verdict: 'true' })}
                                    style={{
                                        padding: '12px 16px',
                                        background: reportData.verdict === 'true' ? 'var(--success)' : 'var(--bg-secondary)',
                                        border: `2px solid ${reportData.verdict === 'true' ? 'var(--success)' : 'var(--border-color)'}`,
                                        borderRadius: '6px',
                                        color: reportData.verdict === 'true' ? 'white' : 'var(--text-primary)',
                                        cursor: 'pointer',
                                        fontWeight: 600,
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '8px',
                                        transition: 'all 0.3s'
                                    }}
                                >
                                    <CheckCircle size={16} />
                                    True
                                </button>
                                <button
                                    onClick={() => setReportData({ ...reportData, verdict: 'false' })}
                                    style={{
                                        padding: '12px 16px',
                                        background: reportData.verdict === 'false' ? 'var(--danger)' : 'var(--bg-secondary)',
                                        border: `2px solid ${reportData.verdict === 'false' ? 'var(--danger)' : 'var(--border-color)'}`,
                                        borderRadius: '6px',
                                        color: reportData.verdict === 'false' ? 'white' : 'var(--text-primary)',
                                        cursor: 'pointer',
                                        fontWeight: 600,
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '8px',
                                        transition: 'all 0.3s'
                                    }}
                                >
                                    <XCircle size={16} />
                                    False
                                </button>
                            </div>
                        </div>

                        <div style={{ marginBottom: '20px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontWeight: 600, color: 'var(--text-primary)' }}>
                                Evidence URLs (Optional)
                            </label>
                            {reportData.evidence.map((url, index) => (
                                <div key={index} style={{ marginBottom: '10px', display: 'flex', gap: '8px' }}>
                                    <input
                                        type="url"
                                        value={url}
                                        onChange={(e) => updateEvidence(index, e.target.value)}
                                        placeholder="https://example.com/proof"
                                        style={{
                                            flex: 1,
                                            padding: '10px',
                                            border: '1px solid var(--border-color)',
                                            borderRadius: '6px',
                                            background: 'var(--bg-secondary)',
                                            color: 'var(--text-primary)',
                                            fontSize: '0.9rem'
                                        }}
                                    />
                                </div>
                            ))}
                            <button
                                onClick={addEvidenceField}
                                style={{
                                    padding: '8px 12px',
                                    background: 'var(--bg-secondary)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: '6px',
                                    color: 'var(--text-primary)',
                                    cursor: 'pointer',
                                    fontSize: '0.85rem'
                                }}
                            >
                                + Add Evidence URL
                            </button>
                        </div>

                        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                            <button
                                onClick={() => {
                                    setShowReportModal(null);
                                    setReportData({ verdict: '', evidence: [''] });
                                }}
                                style={{
                                    padding: '12px 24px',
                                    background: 'var(--bg-secondary)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: '6px',
                                    color: 'var(--text-primary)',
                                    cursor: 'pointer',
                                    fontWeight: 600
                                }}
                            >
                                Cancel
                            </button>
                            <button
                                onClick={() => handleSubmitReport(showReportModal)}
                                disabled={!reportData.verdict || submittingReport === showReportModal}
                                style={{
                                    padding: '12px 24px',
                                    background: submittingReport === showReportModal ? 'var(--text-tertiary)' : 'var(--accent-primary)',
                                    border: 'none',
                                    borderRadius: '6px',
                                    color: 'white',
                                    cursor: submittingReport === showReportModal ? 'not-allowed' : 'pointer',
                                    fontWeight: 600,
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '8px'
                                }}
                            >
                                {submittingReport === showReportModal ? (
                                    <>
                                        <Loader2 size={16} className="animate-spin" />
                                        Submitting...
                                    </>
                                ) : (
                                    <>
                                        <CheckCircle size={16} />
                                        Submit Report
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Info Box */}
            <div style={{
                marginTop: '32px',
                padding: '20px',
                background: 'linear-gradient(135deg, rgba(122, 74, 46, 0.15), rgba(156, 163, 175, 0.1))',
                borderLeft: '4px solid var(--accent-primary)',
                borderRadius: '8px',
                fontSize: '0.9rem',
                color: 'var(--text-secondary)'
            }}>
                <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: '6px' }}>📊 How Oracle Consensus Works</div>
                <div>Markets resolve when 60% of oracle votes agree. Oracles with higher reputation scores have more voting power. Accurate voters are rewarded with reputation points and CC.</div>
            </div>
        </div>
    );
};

export default Oracle;

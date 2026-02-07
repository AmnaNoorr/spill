import React, { useEffect, useState } from 'react';
import '../styles/variables.css';

const SplashScreen = ({ onComplete }) => {
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsVisible(false);
            setTimeout(onComplete, 500); // Wait for fade out
        }, 2500);
        return () => clearTimeout(timer);
    }, [onComplete]);

    if (!isVisible) return null;

    return (
        <div className={`splash-screen ${!isVisible ? 'hidden' : ''}`} style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100vh',
            background: 'linear-gradient(135deg, #8b5a3c 0%, #5c3a32 100%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 9999,
            transition: 'opacity 0.5s, visibility 0.5s',
            opacity: isVisible ? 1 : 0,
            visibility: isVisible ? 'visible' : 'hidden'
        }}>
            {/* Animated background elements */}
            <div style={{
                position: 'absolute',
                width: '500px',
                height: '500px',
                background: 'radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%)',
                borderRadius: '50%',
                top: '-150px',
                left: '-100px'
            }}></div>
            <div style={{
                position: 'absolute',
                width: '350px',
                height: '350px',
                background: 'radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%)',
                borderRadius: '50%',
                bottom: '-100px',
                right: '-50px'
            }}></div>

            {/* Content */}
            <div style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
                {/* Teacup Animation */}
                <div style={{
                    position: 'relative',
                    width: '200px',
                    height: '200px',
                    marginBottom: '50px',
                    animation: 'float 3s ease-in-out infinite'
                }}>
                    {/* Steam */}
                    <div style={{
                        position: 'absolute',
                        top: '-50px',
                        left: '50%',
                        transform: 'translateX(-50%)',
                        display: 'flex',
                        gap: '8px'
                    }}>
                        <span style={{
                            display: 'block',
                            width: '8px',
                            height: '35px',
                            background: 'rgba(248, 244, 237, 0.65)',
                            borderRadius: '50%',
                            filter: 'blur(6px)',
                            animation: 'steam 3s ease-out infinite',
                            animationDelay: '0s'
                        }}></span>
                        <span style={{
                            display: 'block',
                            width: '8px',
                            height: '35px',
                            background: 'rgba(248, 244, 237, 0.65)',
                            borderRadius: '50%',
                            filter: 'blur(6px)',
                            animation: 'steam 3s ease-out infinite',
                            animationDelay: '0.5s'
                        }}></span>
                        <span style={{
                            display: 'block',
                            width: '8px',
                            height: '35px',
                            background: 'rgba(248, 244, 237, 0.65)',
                            borderRadius: '50%',
                            filter: 'blur(6px)',
                            animation: 'steam 3s ease-out infinite',
                            animationDelay: '1s'
                        }}></span>
                    </div>

                    {/* Teacup */}
                    <div style={{
                        width: '120px',
                        height: '80px',
                        background: '#faf7f5',
                        borderRadius: '0 0 50px 50px',
                        position: 'absolute',
                        left: '50%',
                        top: '50%',
                        transform: 'translate(-50%, -50%)',
                        border: '4px solid #d4af37',
                        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.3), inset 0 2px 4px rgba(255, 255, 255, 0.3)'
                    }}>
                        {/* Cup Handle */}
                        <div style={{
                            position: 'absolute',
                            width: '40px',
                            height: '50px',
                            border: '4px solid #d4af37',
                            borderLeft: 'none',
                            borderRadius: '0 30px 30px 0',
                            right: '-44px',
                            top: '10px'
                        }}></div>

                        {/* Tea Liquid */}
                        <div style={{
                            position: 'absolute',
                            bottom: 0,
                            left: 0,
                            right: 0,
                            background: 'linear-gradient(180deg, rgba(139, 90, 60, 0.9) 0%, rgba(93, 58, 50, 0.95) 100%)',
                            borderRadius: '0 0 46px 46px',
                            animation: 'teaFill 2s ease-out forwards',
                            height: '70%',
                            boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.2)'
                        }}></div>
                    </div>
                </div>

                {/* Title */}
                <h1 style={{
                    fontFamily: "'Playfair Display', 'Georgia', serif",
                    fontSize: '3.8rem',
                    color: '#f8f4ed',
                    textAlign: 'center',
                    marginBottom: '16px',
                    animation: 'pulse 2s ease-in-out infinite',
                    fontWeight: 700,
                    textShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
                    letterSpacing: '-0.5px'
                }}>SipsNSecrets</h1>

                {/* Subtitle */}
                <p style={{
                    fontSize: '1.3rem',
                    color: '#f8f4ed',
                    textAlign: 'center',
                    fontWeight: 300,
                    letterSpacing: '1.5px',
                    animation: 'fadeIn 2s ease-in',
                    marginBottom: '40px',
                    textShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
                }}>Sip the Tea, Spill the Secrets</p>

                {/* Loading indicator */}
                <div style={{
                    display: 'flex',
                    gap: '8px',
                    justifyContent: 'center',
                    animation: 'fadeIn 2s ease-in'
                }}>
                    <div style={{
                        width: '8px',
                        height: '8px',
                        background: 'rgba(248, 244, 237, 0.7)',
                        borderRadius: '50%',
                        animation: 'pulse 1.5s ease-in-out infinite',
                        animationDelay: '0s'
                    }}></div>
                    <div style={{
                        width: '8px',
                        height: '8px',
                        background: 'rgba(248, 244, 237, 0.7)',
                        borderRadius: '50%',
                        animation: 'pulse 1.5s ease-in-out infinite',
                        animationDelay: '0.2s'
                    }}></div>
                    <div style={{
                        width: '8px',
                        height: '8px',
                        background: 'rgba(248, 244, 237, 0.7)',
                        borderRadius: '50%',
                        animation: 'pulse 1.5s ease-in-out infinite',
                        animationDelay: '0.4s'
                    }}></div>
                </div>
            </div>
        </div>
    );
};

export default SplashScreen;

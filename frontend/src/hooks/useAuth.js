import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

/**
 * Custom hook for authentication
 */
export function useAuth() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    /**
     * Initialize user with pseudonym
     */
    const initialize = async (pseudonym) => {
        try {
            setLoading(true);
            setError(null);
            const response = await authAPI.initialize(pseudonym);
            setUser(response.user);
            // Store user ID in localStorage
            if (response.user?.id) {
                localStorage.setItem('userId', response.user.id);
                localStorage.setItem('pseudonym', response.user.pseudonym);
            }
            return response.user;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    /**
     * Load user from localStorage on mount
     */
    useEffect(() => {
        const userId = localStorage.getItem('userId');
        const pseudonym = localStorage.getItem('pseudonym');
        
        if (userId && pseudonym) {
            // Try to get user data
            authAPI.getUser(userId)
                .then((response) => {
                    setUser(response.user);
                })
                .catch(() => {
                    // If user not found, clear localStorage
                    localStorage.removeItem('userId');
                    localStorage.removeItem('pseudonym');
                })
                .finally(() => {
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, []);

    /**
     * Clear user session
     */
    const logout = () => {
        setUser(null);
        localStorage.removeItem('userId');
        localStorage.removeItem('pseudonym');
    };

    return {
        user,
        loading,
        error,
        initialize,
        logout,
        isAuthenticated: !!user,
    };
}


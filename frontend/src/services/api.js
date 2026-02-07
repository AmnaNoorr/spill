/**
 * API Service for communicating with Flask backend
 * In development: Uses Vite proxy (relative URLs)
 * In production: Uses absolute backend URL from environment
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Generic API request handler
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    };

    if (options.body && typeof options.body === 'object') {
        config.body = JSON.stringify(options.body);
    }

    try {
        const response = await fetch(url, config);
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        let data;
        
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            data = { error: await response.text() };
        }

        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error.message);
        throw new Error(error.message || 'Failed to fetch data from server');
    }
}

// Auth API
export const authAPI = {
    /**
     * Initialize or get existing user
     */
    initialize: async (pseudonym) => {
        return apiRequest('/auth/initialize', {
            method: 'POST',
            body: { pseudonym },
        });
    },

    /**
     * Get user by ID
     */
    getUser: async (userId) => {
        return apiRequest(`/auth/user/${userId}`);
    },

    /**
     * Get top users
     */
    getTopUsers: async () => {
        return apiRequest('/auth/users');
    },
};

// Markets API
export const marketsAPI = {
    /**
     * Get all markets with optional filters
     */
    getMarkets: async (params = {}) => {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = `/markets${queryString ? `?${queryString}` : ''}`;
        return apiRequest(endpoint);
    },

    /**
     * Get market by ID
     */
    getMarket: async (marketId) => {
        return apiRequest(`/markets/${marketId}`);
    },

    /**
     * Submit a new market
     */
    submitMarket: async (marketData) => {
        return apiRequest('/markets/submit', {
            method: 'POST',
            body: marketData,
        });
    },

    /**
     * Place a bet on a market
     */
    placeBet: async (marketId, betData) => {
        return apiRequest(`/markets/${marketId}/bet`, {
            method: 'POST',
            body: betData,
        });
    },

    /**
     * Delete a market (only submitter can delete)
     */
    deleteMarket: async (marketId, userId) => {
        return apiRequest(`/markets/${marketId}/delete`, {
            method: 'DELETE',
            body: { user_id: userId },
        });
    },

    /**
     * Update a market by creating a new version
     */
    updateMarket: async (marketId, updateData) => {
        return apiRequest(`/markets/${marketId}/update`, {
            method: 'POST',
            body: updateData,
        });
    },

    /**
     * Get all versions of a market
     */
    getMarketVersions: async (marketId) => {
        return apiRequest(`/markets/${marketId}/versions`);
    },
};

// Oracle API
export const oracleAPI = {
    /**
     * Resolve a market through oracle consensus
     */
    resolveMarket: async (marketId, outcome = null) => {
        return apiRequest('/oracles/resolve', {
            method: 'POST',
            body: { market_id: marketId, outcome },
        });
    },

    /**
     * Submit oracle report with evidence
     */
    submitReport: async (reportData) => {
        return apiRequest('/oracles/submit', {
            method: 'POST',
            body: reportData,
        });
    },

    /**
     * Get all oracle reports for a market
     */
    getReports: async (marketId) => {
        return apiRequest(`/oracles/reports/${marketId}`);
    },

    /**
     * Get oracle reputation statistics
     */
    getOracleReputation: async (oracleId) => {
        return apiRequest(`/oracles/reputation/${oracleId}`);
    },

    /**
     * Get top oracles by reputation
     */
    getTopOracles: async (limit = 20) => {
        return apiRequest(`/oracles/reputation/top?limit=${limit}`);
    },

    /**
     * Fetch evidence from URLs
     */
    fetchEvidence: async (urls, rumorText, marketId = null) => {
        return apiRequest('/oracles/evidence/fetch', {
            method: 'POST',
            body: { urls, rumor_text: rumorText, market_id: marketId },
        });
    },

    /**
     * Auto-fetch evidence for a market (for bots)
     */
    autoFetchEvidence: async (marketId) => {
        return apiRequest(`/oracles/evidence/auto/${marketId}`, {
            method: 'POST',
        });
    },
};

// Health & Stats API
export const systemAPI = {
    /**
     * Health check
     */
    health: async () => {
        return apiRequest('/health');
    },

    /**
     * Get system statistics
     */
    getStats: async () => {
        return apiRequest('/stats');
    },
};

export default {
    auth: authAPI,
    markets: marketsAPI,
    oracle: oracleAPI,
    system: systemAPI,
};


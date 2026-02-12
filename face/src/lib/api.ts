import axios from 'axios';

// Defaults to localhost:8000 if not set
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor (Auth Token)
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response Interceptor (Error Handling)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            // window.location.href = '/login'; // Simple redirect for now
        }
        return Promise.reject(error);
    }
);

// --- Decision Types ---
export interface Decision {
    action: "REPLY" | "ARCHIVE" | "IGNORE" | "ESCALATE";
    body?: string;
    reasoning: string;
    tags: string[];
}

// --- HITL Types ---
export interface HitlRequest {
    id: string;
    tenant_id: string;
    work_item_id: string;
    reason: string;
    state: "PENDING" | "CLAIMED" | "RESOLVED" | "REJECTED";
    created_at: string; // ISO Date
    claimed_by_agent_id?: string;
}

export interface HitlDecision {
    request_id: string;
    agent_id: string;
    outcome: "RESOLVED" | "REJECTED";
    modified_draft?: string;
    feedback_notes?: string;
}

// --- HITL Endpoints ---
export const hitl = {
    getQueue: async (tenantId: string): Promise<HitlRequest[]> => {
        const response = await api.get('/hitl/queue', { params: { tenant_id: tenantId } });
        return response.data;
    },

    claimRequest: async (requestId: string, agentId: string) => {
        const response = await api.post(`/hitl/claim/${requestId}`, null, { params: { agent_id: agentId } });
        return response.data;
    },

    resolveRequest: async (decision: HitlDecision) => {
        const response = await api.post('/hitl/resolve', decision);
        return response.data;
    }
};

// --- Admin Types ---
export interface Organization {
    id: string;
    name: string;
    created_at: string;
}

export interface Tenant {
    id: string;
    organization_id: string;
    name: string;
    tier: "SOLO" | "PRO" | "BUSINESS" | "ENTERPRISE";
    status: "ACTIVE" | "SUSPENDED" | "ARCHIVED";
    created_at: string;
}

// --- Admin Endpoints ---
export const admin = {
    createOrg: async (name: string): Promise<Organization> => {
        const response = await api.post('/admin/orgs', null, { params: { name } });
        return response.data;
    },

    createTenant: async (orgId: string, name: string, tier: string): Promise<Tenant> => {
        const response = await api.post('/admin/tenants', null, { params: { org_id: orgId, name, tier } });
        return response.data;
    },

    suspendTenant: async (tenantId: string): Promise<Tenant> => {
        const response = await api.post(`/admin/tenants/${tenantId}/suspend`);
        return response.data;
    },

    getHierarchy: async (orgId: string): Promise<{ organization: Organization, tenants: Tenant[] }> => {
        const response = await api.get(`/admin/orgs/${orgId}/hierarchy`);
        return response.data;
    },

    // Not listed in Interface but inferred
    getSafetyStatus: async (): Promise<{ status: "OPERATIONAL" | "HALTED", last_updated: string }> => {
        const response = await api.get('/admin/safety/status');
        return response.data;
    },

    engageKillSwitch: async () => {
        const response = await api.post('/admin/safety/kill');
        return response.data;
    },

    disengageKillSwitch: async () => {
        const response = await api.post('/admin/safety/resume');
        return response.data;
    },

    // Billing
    getPlans: async () => {
        const response = await api.get('/admin/billing/plans');
        return response.data;
    },

    getLedger: async (tenantId: string) => {
        const response = await api.get(`/admin/billing/${tenantId}/ledger`);
        return response.data;
    }
};

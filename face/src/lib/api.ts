import type { WorkItem } from './types';

const API_BASE = '/api/v2/work-items';

export const api = {
    listItems: async (): Promise<WorkItem[]> => {
        const res = await fetch(API_BASE);
        if (!res.ok) throw new Error('Failed to list items');
        return res.json();
    },

    getItem: async (id: string): Promise<WorkItem> => {
        const res = await fetch(`${API_BASE}/${id}`);
        if (!res.ok) throw new Error('Failed to get item');
        return res.json();
    },

    triggerDraft: async (id: string): Promise<void> => {
        const res = await fetch(`${API_BASE}/${id}/draft`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed to trigger draft');
    },

    approveDraft: async (id: string): Promise<void> => {
        const res = await fetch(`${API_BASE}/${id}/approve`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed to approve draft');
    },

    // Generic methods for other endpoints (e.g. /emails, /auth)
    get: async (url: string): Promise<any> => {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`GET ${url} failed`);
        return res.json();
    },

    post: async (url: string, body?: any): Promise<any> => {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body ? JSON.stringify(body) : undefined
        });
        if (!res.ok) throw new Error(`POST ${url} failed`);
        return res.json();
    }
};

export const admin = {
    suspendTenant: async (id: string): Promise<void> => {
        const res = await fetch(`${API_BASE}/../admin/tenants/${id}/suspend`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed to suspend tenant');
    }
};

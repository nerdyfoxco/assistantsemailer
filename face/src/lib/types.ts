export interface ItemContext {
    body: string;
    tone: string;
}

export interface WorkItem {
    id: string;
    tenant_id: string;
    state: 'NEW' | 'DRAFTING' | 'REVIEW' | 'SENDING' | 'CLOSED';
    source_message_id: string;
    payload?: any;
    draft_context?: ItemContext;
}

export interface Tenant {
    id: string;
    name: string;
    tier: string;
    status: 'ACTIVE' | 'SUSPENDED';
    created_at: string;
}

export type WorkItemState = WorkItem['state'];

export interface WorkflowState {
    workflow_id: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    current_step_id?: string;
    data: Record<string, unknown>;
    created_at: string;
    updated_at: string;
}

export interface WorkflowRepository {
    save(state: WorkflowState): Promise<void>;
    load(workflowId: string): Promise<WorkflowState | null>;
}

export class InMemoryWorkflowRepository implements WorkflowRepository {
    private storage = new Map<string, WorkflowState>();

    async save(state: WorkflowState): Promise<void> {
        this.storage.set(state.workflow_id, { ...state }); // Store copy
    }

    async load(workflowId: string): Promise<WorkflowState | null> {
        const state = this.storage.get(workflowId);
        return state ? { ...state } : null; // Return copy
    }
}

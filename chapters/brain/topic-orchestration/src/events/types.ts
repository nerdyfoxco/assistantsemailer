export interface WorkflowStartedEvent {
    meta: {
        event_id: string;
        timestamp_utc: string;
        correlation_id: string;
        producer: string;
        schema_version: '1.0.0';
    };
    data: {
        workflow_id: string;
        workflow_name: string;
        initiator: string;
        inputs?: Record<string, unknown>;
    };
}

export interface StepCompletedEvent {
    meta: {
        event_id: string;
        timestamp_utc: string;
        correlation_id: string;
        producer: string;
        schema_version: '1.0.0';
    };
    data: {
        workflow_id: string;
        step_id: string;
        step_name: string;
        status: 'success' | 'failure';
        outputs?: Record<string, unknown>;
    };
}

export interface StepScheduledEvent {
    meta: {
        event_id: string;
        timestamp_utc: string;
        correlation_id: string;
        producer: string;
        schema_version: '1.0.0';
    };
    data: {
        workflow_id: string;
        step_id: string;
        step_name?: string;
        step_type: 'function' | 'api_call' | 'human_review';
        inputs?: Record<string, unknown>;
    };
}

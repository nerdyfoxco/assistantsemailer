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
        step_name?: string; // Added optional step_name
        step_type: string;  // Relaxed from hardcoded union to string for extensibility
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
        step_name?: string; // Optional request, optional response
        status: 'success' | 'failure';
        outputs?: Record<string, unknown>;
    };
}

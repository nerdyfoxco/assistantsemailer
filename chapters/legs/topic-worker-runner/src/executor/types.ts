export interface StepContext {
    workflow_id: string;
    step_id: string;
    correlation_id: string;
}

export interface StepHandler {
    type: string;
    handle(inputs: Record<string, unknown>, context: StepContext): Promise<Record<string, unknown>>;
}

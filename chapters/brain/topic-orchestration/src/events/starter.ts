import { EventEmitter } from 'events';
import { WorkflowStartedEvent } from './types';

export declare interface WorkflowStartConsumer {
    on(event: 'startOrchestration', listener: (payload: WorkflowStartedEvent) => void): this;
}

export class WorkflowStartConsumer extends EventEmitter {
    public handleWorkflowStarted(event: unknown): void {
        if (!this.isValidEvent(event)) {
            throw new Error('Invalid workflow.started event payload');
        }
        this.emit('startOrchestration', event);
    }

    private isValidEvent(event: unknown): event is WorkflowStartedEvent {
        const e = event as Partial<WorkflowStartedEvent>;
        return (
            typeof e === 'object' &&
            e !== null &&
            e.meta?.schema_version === '1.0.0' &&
            e.data?.workflow_id !== undefined
        );
    }
}

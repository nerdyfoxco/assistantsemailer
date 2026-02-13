import { EventEmitter } from 'events';
import { StepCompletedEvent } from './types';

export declare interface WorkflowConsumer {
    on(event: 'stepCompleted', listener: (payload: StepCompletedEvent) => void): this;
}

export class WorkflowConsumer extends EventEmitter {
    /**
     * Ingests a raw event from the pipe.
     * In a real system, this would be called by the transport layer (e.g., RabbitMQ/Kafka consumer).
     * For UMP-0005, we expose it directly to simulate transport delivery.
     */
    public handleStepCompleted(event: unknown): void {
        if (!this.isValidEvent(event)) {
            throw new Error('Invalid step.completed event payload');
        }

        // Emit fully typed internal event for business logic to consume
        this.emit('stepCompleted', event);
    }

    private isValidEvent(event: unknown): event is StepCompletedEvent {
        // Basic runtime validation (in addition to contract tests)
        const e = event as Partial<StepCompletedEvent>;
        return (
            typeof e === 'object' &&
            e !== null &&
            e.meta?.schema_version === '1.0.0' &&
            Array.isArray(e.meta.producer.match(/chapters\/legs\/.+/)) === true
            // Real validation should use the AJV runner, but for this UMP we do basic structural check
            && typeof e.data?.step_id === 'string'
            && (e.data.status === 'success' || e.data.status === 'failure')
        );
    }
}

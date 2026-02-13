import { EventEmitter } from 'events';
import * as crypto from 'crypto';
import { WorkflowStartedEvent } from './types';

export class WorkflowProducer extends EventEmitter {
    public emitWorkflowStarted(
        correlationId: string,
        data: Omit<WorkflowStartedEvent['data'], 'inputs'> & { inputs?: Record<string, unknown> }
    ): WorkflowStartedEvent {

        const event: WorkflowStartedEvent = {
            meta: {
                event_id: crypto.randomUUID(),
                timestamp_utc: new Date().toISOString(),
                correlation_id: correlationId,
                producer: 'chapters/brain/topic-orchestration',
                schema_version: '1.0.0'
            },
            data
        };

        this.emit('pipe.workflow.started.v1', event);
        return event;
    }
}

import { EventEmitter } from 'events';
import * as crypto from 'crypto';
import { StepCompletedEvent } from './types';

export class WorkerProducer extends EventEmitter {
    public emitStepCompleted(
        correlationId: string,
        data: Omit<StepCompletedEvent['data'], 'outputs'> & { outputs?: Record<string, unknown> }
    ): StepCompletedEvent {

        const event: StepCompletedEvent = {
            meta: {
                event_id: crypto.randomUUID(),
                timestamp_utc: new Date().toISOString(),
                correlation_id: correlationId,
                producer: 'chapters/legs/topic-worker-runner',
                schema_version: '1.0.0'
            },
            data
        };

        this.emit('pipe.workflow.step.completed.v1', event);
        return event;
    }
}

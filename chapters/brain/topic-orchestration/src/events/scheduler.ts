import { EventEmitter } from 'events';
import * as crypto from 'crypto';
import { StepScheduledEvent } from './types';

export class StepScheduler extends EventEmitter {
    public scheduleStep(
        correlationId: string,
        data: Omit<StepScheduledEvent['data'], 'step_type'> & { step_type: StepScheduledEvent['data']['step_type'] }
    ): StepScheduledEvent {

        const event: StepScheduledEvent = {
            meta: {
                event_id: crypto.randomUUID(),
                timestamp_utc: new Date().toISOString(),
                correlation_id: correlationId,
                producer: 'chapters/brain/topic-orchestration',
                schema_version: '1.0.0'
            },
            data
        };

        // Emit to pipe
        this.emit('pipe.step.scheduled.v1', event);
        return event;
    }
}

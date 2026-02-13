import { EventEmitter } from 'events';
import { StepScheduledEvent } from './types';
import { WorkerDispatcher } from '../executor/dispatcher';

export declare interface WorkerConsumer {
    on(event: 'executeStep', listener: (payload: { event: StepScheduledEvent, resolve: (out: any) => void, reject: (err: any) => void }) => void): this;
    on(event: 'stepExecuted', listener: (payload: { event: StepScheduledEvent, outputs: any, status: 'success' | 'failure' }) => void): this;
}

export class WorkerConsumer extends EventEmitter {
    constructor(private dispatcher?: WorkerDispatcher) {
        super();
    }

    public async handleStepScheduled(event: unknown): Promise<void> {
        if (this.isValidEvent(event)) {
            console.log(`[WorkerConsumer] Received step: ${event.data.step_id} (${event.data.step_type})`);

            if (this.dispatcher) {
                // Real Execution Path
                try {
                    const outputs = await this.dispatcher.dispatch(
                        event.data.step_type,
                        event.data.inputs || {},  // Ensure inputs is object
                        {
                            workflow_id: event.data.workflow_id,
                            step_id: event.data.step_id,
                            correlation_id: event.meta.correlation_id
                        }
                    );
                    this.emit('stepExecuted', { event, outputs, status: 'success' });
                } catch (err: any) {
                    console.error(`[WorkerConsumer] Execution Failed:`, err);
                    this.emit('stepExecuted', { event, outputs: { error: err.message }, status: 'failure' });
                }
            } else {
                // Legacy/Simulation Path
                this.emit('executeStep', {
                    event,
                    resolve: (o: any) => this.emit('stepExecuted', { event, outputs: o, status: 'success' }),
                    reject: (e: any) => this.emit('stepExecuted', { event, outputs: { error: e.message }, status: 'failure' })
                });
            }
        }
    }

    private isValidEvent(event: unknown): event is StepScheduledEvent {
        const e = event as Partial<StepScheduledEvent>;
        return (
            typeof e === 'object' &&
            e !== null &&
            e.meta?.schema_version === '1.0.0' &&
            typeof e.data?.step_id === 'string' &&
            typeof e.data?.step_type === 'string'
        );
    }
}

import { test } from 'node:test';
import assert from 'node:assert';
import { StepScheduler } from '../src/events/scheduler';
import { StepScheduledEvent } from '../src/events/types';

test('StepScheduler emits valid step.scheduled event', async () => {
    const scheduler = new StepScheduler();
    const correlationId = 'test-corr-sched';
    const stepData = {
        workflow_id: 'wf-sched',
        step_id: 'step-1',
        step_type: 'function' as const,
        inputs: { task: 'do-it' }
    };

    return new Promise<void>((resolve, reject) => {
        scheduler.on('pipe.step.scheduled.v1', (event: StepScheduledEvent) => {
            try {
                assert.strictEqual(event.meta.correlation_id, correlationId);
                assert.strictEqual(event.meta.producer, 'chapters/brain/topic-orchestration');
                assert.strictEqual(event.data.step_id, stepData.step_id);
                assert.strictEqual(event.data.step_type, 'function');
                resolve();
            } catch (err) {
                reject(err);
            }
        });

        scheduler.scheduleStep(correlationId, stepData);
    });
});

import { test } from 'node:test';
import assert from 'node:assert';
import { WorkerProducer } from '../src/events/producer';
import { StepCompletedEvent } from '../src/events/types';

test('WorkerProducer emits valid step.completed event', async () => {
    const producer = new WorkerProducer();
    const correlationId = 'test-corr-1';
    const stepData = {
        workflow_id: 'wf-1',
        step_id: 'step-1',
        step_name: 'test-step',
        status: 'success' as const
    };

    return new Promise<void>((resolve, reject) => {
        producer.on('pipe.workflow.step.completed.v1', (event: StepCompletedEvent) => {
            try {
                assert.strictEqual(event.meta.correlation_id, correlationId);
                assert.strictEqual(event.meta.producer, 'chapters/legs/topic-worker-runner');
                assert.strictEqual(event.data.step_id, stepData.step_id);
                assert.strictEqual(event.data.status, 'success');
                resolve();
            } catch (err) {
                reject(err);
            }
        });

        producer.emitStepCompleted(correlationId, stepData);
    });
});

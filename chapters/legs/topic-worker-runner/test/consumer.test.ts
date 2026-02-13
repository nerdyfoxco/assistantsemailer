import { test } from 'node:test';
import assert from 'node:assert';
import { WorkerConsumer } from '../src/events/consumer';
import { StepScheduledEvent } from '../src/events/types';

test('WorkerConsumer handles valid step.scheduled event', async () => {
    const consumer = new WorkerConsumer();
    const validEvent: StepScheduledEvent = {
        meta: {
            event_id: 'evt-1',
            timestamp_utc: new Date().toISOString(),
            correlation_id: 'corr-1',
            producer: 'chapters/brain/topic-orchestration',
            schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-1',
            step_id: 'step-1',
            step_type: 'function',
            inputs: { foo: 'bar' }
        }
    };

    return new Promise<void>((resolve) => {
        consumer.on('executeStep', (event) => {
            assert.deepStrictEqual(event, validEvent);
            resolve();
        });
        consumer.handleStepScheduled(validEvent);
    });
});

test('WorkerConsumer rejects invalid event', () => {
    const consumer = new WorkerConsumer();
    const invalidEvent = {
        meta: { schema_version: '1.0.0' },
        data: { step_type: 'bad-type' }
    };

    assert.throws(() => {
        consumer.handleStepScheduled(invalidEvent);
    }, /Invalid step.scheduled event/);
});

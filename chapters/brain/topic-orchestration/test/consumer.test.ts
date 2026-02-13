import { test } from 'node:test';
import assert from 'node:assert';
import { WorkflowConsumer } from '../src/events/consumer';
import { StepCompletedEvent } from '../src/events/types';

test('WorkflowConsumer handles valid step.completed event', async () => {
    const consumer = new WorkflowConsumer();
    const validEvent: StepCompletedEvent = {
        meta: {
            event_id: 'evt-123',
            timestamp_utc: new Date().toISOString(),
            correlation_id: 'corr-123',
            producer: 'chapters/legs/topic-worker-runner',
            schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-abc',
            step_id: 'step-1',
            step_name: 'email-send',
            status: 'success'
        }
    };

    return new Promise<void>((resolve) => {
        consumer.on('stepCompleted', (event) => {
            assert.deepStrictEqual(event, validEvent);
            resolve();
        });

        consumer.handleStepCompleted(validEvent);
    });
});

test('WorkflowConsumer rejects invalid event', () => {
    const consumer = new WorkflowConsumer();
    const invalidEvent = {
        meta: { schema_version: '0.0.9' }, // Bad version
        data: {}
    };

    assert.throws(() => {
        consumer.handleStepCompleted(invalidEvent);
    }, /Invalid step.completed event/);
});

import { test } from 'node:test';
import assert from 'node:assert';
import { WorkflowStartConsumer } from '../src/events/starter';
import { WorkflowStartedEvent } from '../src/events/types';

test('WorkflowStartConsumer handles valid workflow.started event', async () => {
    const consumer = new WorkflowStartConsumer();
    const validEvent: WorkflowStartedEvent = {
        meta: {
            event_id: 'evt-start-1',
            timestamp_utc: new Date().toISOString(),
            correlation_id: 'corr-start-1',
            producer: 'api',
            schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-start-1',
            workflow_name: 'onboarding',
            initiator: 'user'
        }
    };

    return new Promise<void>((resolve) => {
        consumer.on('startOrchestration', (event) => {
            assert.deepStrictEqual(event, validEvent);
            resolve();
        });
        consumer.handleWorkflowStarted(validEvent);
    });
});

test('WorkflowStartConsumer rejects invalid event', () => {
    const consumer = new WorkflowStartConsumer();
    const invalidEvent = {
        meta: { schema_version: '0.0.0' },
        data: {}
    };

    assert.throws(() => {
        consumer.handleWorkflowStarted(invalidEvent);
    }, /Invalid workflow.started event/);
});

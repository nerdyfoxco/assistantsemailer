import { test } from 'node:test';
import assert from 'node:assert';
import { WorkflowProducer } from '../src/events/producer';
import { WorkflowStartedEvent } from '../src/events/types';

test('WorkflowProducer emits valid workflow.started event', async () => {
    const producer = new WorkflowProducer();
    const correlationId = 'test-corr-123';
    const workflowData = {
        workflow_id: 'wf-abc',
        workflow_name: 'test-workflow',
        initiator: 'tester'
    };

    return new Promise<void>((resolve, reject) => {
        producer.on('pipe.workflow.started.v1', (event: WorkflowStartedEvent) => {
            try {
                assert.strictEqual(event.meta.correlation_id, correlationId);
                assert.strictEqual(event.meta.producer, 'chapters/brain/topic-orchestration');
                assert.strictEqual(event.meta.schema_version, '1.0.0');
                assert.strictEqual(event.data.workflow_id, workflowData.workflow_id);
                assert.ok(event.meta.event_id, 'event_id should exist');
                assert.ok(event.meta.timestamp_utc, 'timestamp should exist');
                resolve();
            } catch (err) {
                reject(err);
            }
        });

        producer.emitWorkflowStarted(correlationId, workflowData);
    });
});

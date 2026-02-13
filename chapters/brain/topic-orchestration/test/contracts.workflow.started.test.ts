import { test } from 'node:test';
import assert from 'node:assert';
import { ContractRunner } from '../../../../foundation/src/testing/contract-runner';

const runner = new ContractRunner();
const PIPE_ID = 'pipe.workflow.started.v1';

test(`Contract Test: ${PIPE_ID} - Valid Payload`, () => {
    const payload = {
        meta: {
            event_id: '123e4567-e89b-12d3-a456-426614174000',
            timestamp_utc: '2023-10-01T12:00:00Z',
            correlation_id: 'test-correlation',
            producer: 'brain',
            schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-123',
            workflow_name: 'onboarding',
            initiator: 'user-1'
        }
    };

    const result = runner.validate(PIPE_ID, payload);
    if (!result.valid) {
        console.error(result.errors);
    }
    assert.strictEqual(result.valid, true, 'Valid payload should pass');
});

test(`Contract Test: ${PIPE_ID} - Invalid Payload (Missing Meta)`, () => {
    const payload = {
        data: {
            workflow_id: 'wf-123'
        }
    };

    const result = runner.validate(PIPE_ID, payload);
    assert.strictEqual(result.valid, false, 'Invalid payload should fail');
});

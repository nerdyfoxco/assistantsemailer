import { test } from 'node:test';
import assert from 'node:assert';
import { ContractRunner } from '../../../../foundation/src/testing/contract-runner';

const runner = new ContractRunner();
const PIPE_ID = 'pipe.workflow.step.completed.v1';

test(`Contract Test: ${PIPE_ID} - Valid Payload`, () => {
    const payload = {
        meta: {
            event_id: '123e4567-e89b-12d3-a456-426614174000',
            timestamp_utc: '2023-10-01T12:00:00Z',
            correlation_id: 'test-correlation',
            producer: 'legs',
            schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-123',
            step_id: 'step-1',
            step_name: 'email-send',
            status: 'success'
        }
    };

    const result = runner.validate(PIPE_ID, payload);
    if (!result.valid) {
        console.error(result.errors);
    }
    assert.strictEqual(result.valid, true, 'Valid payload should pass');
});

test(`Contract Test: ${PIPE_ID} - Invalid Payload (Bad Enum)`, () => {
    const payload = {
        meta: {
            event_id: '123e4567-e89b-12d3-a456-426614174000',
            timestamp_utc: '2023-10-01T12:00:00Z',
            correlation_id: 'test-correlation',
            producer: 'legs',
            schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-123',
            step_id: 'step-1',
            step_name: 'email-send',
            status: 'kinda-ok' // Invalid enum
        }
    };

    const result = runner.validate(PIPE_ID, payload);
    assert.strictEqual(result.valid, false, 'Invalid enum should fail');
});

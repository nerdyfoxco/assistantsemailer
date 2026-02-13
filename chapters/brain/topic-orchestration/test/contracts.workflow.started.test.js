"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const node_test_1 = require("node:test");
const node_assert_1 = __importDefault(require("node:assert"));
const contract_runner_1 = require("../../../../foundation/src/testing/contract-runner");
const runner = new contract_runner_1.ContractRunner();
const PIPE_ID = 'pipe.workflow.started.v1';
(0, node_test_1.test)(`Contract Test: ${PIPE_ID} - Valid Payload`, () => {
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
    node_assert_1.default.strictEqual(result.valid, true, 'Valid payload should pass');
});
(0, node_test_1.test)(`Contract Test: ${PIPE_ID} - Invalid Payload (Missing Meta)`, () => {
    const payload = {
        data: {
            workflow_id: 'wf-123'
        }
    };
    const result = runner.validate(PIPE_ID, payload);
    node_assert_1.default.strictEqual(result.valid, false, 'Invalid payload should fail');
});

import { test } from 'node:test';
import assert from 'node:assert';
import { MathHandler } from '../src/handlers/math';

test('MathHandler adds two numbers', async () => {
    const handler = new MathHandler();
    const context = { workflow_id: '1', step_id: '1', correlation_id: '1' };

    const result = await handler.handle({ a: 5, b: 10 }, context);
    assert.strictEqual(result['result'], 15);
});

test('MathHandler throws on invalid inputs', async () => {
    const handler = new MathHandler();
    const context = { workflow_id: '1', step_id: '1', correlation_id: '1' };

    await assert.rejects(async () => {
        await handler.handle({ a: '5', b: 10 }, context);
    }, /requires inputs/);
});

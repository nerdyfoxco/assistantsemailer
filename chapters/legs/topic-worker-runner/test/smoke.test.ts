import { test } from 'node:test';
import assert from 'node:assert';
import { startServer } from '../src/server';

test('smoke test: worker service starts and responds to /healthz', async () => {
    const TEST_PORT = 3002; // Avoid collision with brain (3001?) or logic.
    const serverInstance = await startServer({ port: TEST_PORT });

    try {
        const response = await fetch(`http://localhost:${TEST_PORT}/healthz`);
        assert.strictEqual(response.status, 200);
        const body = await response.json();
        assert.strictEqual(body.status, 'ok');
        assert.strictEqual(body.service, 'legs-worker-runner');
    } finally {
        await serverInstance.close();
    }
});

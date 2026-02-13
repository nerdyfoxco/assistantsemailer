import { test } from 'node:test';
import assert from 'node:assert';
import * as http from 'http';
import { HttpHandler } from '../src/handlers/http';

test('HttpHandler performs GET request', async () => {
    // Setup Mock Server
    const server = http.createServer((req, res) => {
        if (req.url === '/test') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ hello: 'world' }));
        } else {
            res.writeHead(404);
            res.end();
        }
    });

    await new Promise<void>(resolve => server.listen(0, resolve));
    const port = (server.address() as any).port;
    const url = `http://localhost:${port}/test`;

    try {
        const handler = new HttpHandler();
        const context = { workflow_id: '1', step_id: '1', correlation_id: '1' };

        const result = await handler.handle({ url, method: 'GET' }, context);

        assert.strictEqual(result['status'], 200);
        assert.strictEqual(JSON.parse(result['body'] as string).hello, 'world');

    } finally {
        server.close();
    }
});

const http = require('http');
const { spawn } = require('child_process');

function request(port, path, method, body) {
    return new Promise((resolve, reject) => {
        const req = http.request({
            hostname: 'localhost',
            port: port,
            path: path,
            method: method,
            headers: { 'Content-Type': 'application/json' }
        }, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
        });
        req.on('error', reject);
        if (body) req.write(JSON.stringify(body));
        req.end();
    });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
    console.log('=== Starting Phase 9 Verification ===');

    const brain = spawn('node', ['chapters/brain/topic-orchestration/dist/src/index.js'], { env: { ...process.env, PORT: '3005' }, stdio: 'inherit' });
    const legs = spawn('node', ['chapters/legs/topic-worker-runner/dist/src/index.js'], { env: { ...process.env, PORT: '3006' }, stdio: 'inherit' });

    await sleep(2000);

    try {
        // 1. Trigger Math Workflow (Simulate Brain scheduling it)
        // Note: We are mocking the Brain->Legs scheduling by hitting Legs directly for this test
        // because the Brain logic is currently hardcoded to "initial-step".
        // To properly test End-to-End with Brain, we'd need to update Brain Engine or send a specific payload.
        // For now, let's test Legs capabilities directly via its HTTP endpoint.

        console.log('>>> Testing Math Handler (Direct to Legs)...');
        const mathRes = await request(3006, '/v1/step/schedule', 'POST', {
            meta: { event_id: '1', timestamp_utc: 'now', correlation_id: 'corr-math', producer: 'tester', schema_version: '1.0.0' },
            data: { workflow_id: 'wf-math', step_id: 'step-math', step_type: 'math.add', inputs: { a: 10, b: 32 } }
        });
        console.log('Math Response:', mathRes.statusCode); // Expect 200 (Accepted)

        // Legs logs should show "10 + 32 = 42"

        await sleep(1000);

        // 2. Trigger HTTP Handler
        console.log('>>> Testing HTTP Handler (Direct to Legs)...');
        const httpRes = await request(3006, '/v1/step/schedule', 'POST', {
            meta: { event_id: '2', timestamp_utc: 'now', correlation_id: 'corr-http', producer: 'tester', schema_version: '1.0.0' },
            data: { workflow_id: 'wf-http', step_id: 'step-http', step_type: 'http.request', inputs: { url: 'https://example.com', method: 'GET' } }
        });
        console.log('HTTP Response:', httpRes.statusCode); // Expect 200 (Accepted)

        // Legs logs should show request to example.com

        await sleep(2000);

    } catch (err) {
        console.error(err);
        process.exitCode = 1;
    } finally {
        brain.kill();
        legs.kill();
        console.log('=== Phase 9 Verification Finished ===');
    }
}

main();

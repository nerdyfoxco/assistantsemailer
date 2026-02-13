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
    console.log('=== Starting HTTP Verification ===');

    // Start Brain
    const brain = spawn('node', ['chapters/brain/topic-orchestration/dist/src/index.js'], {
        env: { ...process.env, PORT: '3003' }, // Use 3003 to avoid conflicts
        stdio: 'inherit'
    });

    // Start Legs
    const legs = spawn('node', ['chapters/legs/topic-worker-runner/dist/src/index.js'], {
        env: { ...process.env, PORT: '3004' },
        stdio: 'inherit'
    });

    console.log('Waiting for servers to boot...');
    await sleep(2000);

    try {
        // Health Checks
        const brainHealth = await request(3003, '/healthz', 'GET');
        console.log('Brain Health:', brainHealth.statusCode);
        if (brainHealth.statusCode !== 200) throw new Error('Brain unhealthy');

        const legsHealth = await request(3004, '/healthz', 'GET');
        console.log('Legs Health:', legsHealth.statusCode);
        if (legsHealth.statusCode !== 200) throw new Error('Legs unhealthy');

        // Trigger Workflow
        console.log('>>> Triggering Workflow Start (HTTP)...');
        const startRes = await request(3003, '/v1/workflow/start', 'POST', {
            meta: {
                event_id: 'http-1', timestamp_utc: new Date().toISOString(), correlation_id: 'corr-http', producer: 'tester', schema_version: '1.0.0'
            },
            data: { workflow_id: 'wf-http', workflow_name: 'http-flow', initiator: 'curl' }
        });
        console.log('Start Response:', startRes.statusCode, startRes.body);

        // Logs should show Brain Engine starting and emitting step.scheduled
        // Since we don't have a real bus, we can't automatically catch the output and forward it.
        // But we can verify that the API accepted the request.

        // We can also Manually Schedule a step on Legs to verify its API
        console.log('>>> Scheduling Step on Legs (HTTP)...');
        const schedRes = await request(3004, '/v1/step/schedule', 'POST', {
            meta: {
                event_id: 'http-2', timestamp_utc: new Date().toISOString(), correlation_id: 'corr-http', producer: 'brain-mock', schema_version: '1.0.0'
            },
            data: { workflow_id: 'wf-http', step_id: 'step-99', step_type: 'function', inputs: {} }
        });
        console.log('Schedule Response:', schedRes.statusCode, schedRes.body);

        await sleep(1000);

    } catch (err) {
        console.error('Test Failed:', err);
        process.exitCode = 1;
    } finally {
        brain.kill();
        legs.kill();
        console.log('=== HTTP Verification Finished ===');
    }
}

main();

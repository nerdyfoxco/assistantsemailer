const { Pool } = require('pg');
const http = require('http');

const DB_URL = 'postgresql://admin:password@localhost:5432/email_systems';

async function request(options, body) {
    return new Promise((resolve, reject) => {
        const req = http.request(options, (res) => {
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

async function pollForCompletion(pool, workflowId) {
    for (let i = 0; i < 20; i++) { // 10 seconds timeout
        const res = await pool.query('SELECT * FROM workflows WHERE id = $1', [workflowId]);
        if (res.rows.length > 0) {
            const row = res.rows[0];
            if (row.status === 'completed') {
                return row;
            }
            if (row.status === 'failed') {
                throw new Error(`Workflow failed: ${JSON.stringify(row.data)}`);
            }
        }
        await sleep(500);
    }
    throw new Error('Timeout waiting for workflow completion');
}

async function main() {
    console.log('=== Starting E2E Docker Verification ===');

    const pool = new Pool({ connectionString: DB_URL });

    try {
        // 1. Math Workflow
        const mathId = 'e2e-math-' + Date.now();
        console.log(`[E2E] Triggering Math Workflow (${mathId})...`);

        await request({
            hostname: 'localhost', port: 3000, path: '/v1/workflow/start', method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        }, {
            meta: { event_id: '1', timestamp_utc: 'now', correlation_id: mathId, producer: 'tester', schema_version: '1.0.0' },
            data: {
                workflow_id: mathId,
                initiator: 'tester',
                inputs: { step_type: 'math.add', a: 10, b: 50 }
            }
        });

        const mathRow = await pollForCompletion(pool, mathId);
        console.log('[E2E] Math Workflow Completed:', mathRow.data);

        // Check Result: 10 + 50 = 60
        const mathResult = mathRow.data.outputs?.result;
        if (mathResult !== 60) throw new Error(`Expected 60, got ${mathResult}`);
        console.log('Verified Math Result: 60');

        // 2. HTTP Workflow
        const httpId = 'e2e-http-' + Date.now();
        console.log(`[E2E] Triggering HTTP Workflow (${httpId})...`);

        await request({
            hostname: 'localhost', port: 3000, path: '/v1/workflow/start', method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        }, {
            meta: { event_id: '2', timestamp_utc: 'now', correlation_id: httpId, producer: 'tester', schema_version: '1.0.0' },
            data: {
                workflow_id: httpId,
                initiator: 'tester',
                inputs: { step_type: 'http.request', url: 'http://example.com', method: 'GET' }
            }
        });

        const httpRow = await pollForCompletion(pool, httpId);
        console.log('[E2E] HTTP Workflow Completed. Status Code:', httpRow.data.outputs?.status);

        // Accept 200.
        if (httpRow.data.outputs?.status !== 200) throw new Error(`Expected 200, got ${httpRow.data.outputs?.status}`);
        console.log('Verified HTTP Status: 200');

    } catch (err) {
        console.error(err);
        process.exitCode = 1;
    } finally {
        await pool.end();
        console.log('=== E2E Verification Finished ===');
    }
}

main();

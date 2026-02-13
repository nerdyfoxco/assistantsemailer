const { Client } = require('pg');

const client = new Client({
    connectionString: 'postgresql://admin:password@localhost:5432/email_systems'
});

async function verifyEars() {
    console.log('[Verify] Connecting to Postgres...');
    try {
        await client.connect();
        console.log('[Verify] Connected.');

        // Check if table exists
        const tableCheck = await client.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'workflows'
      );
    `);

        if (!tableCheck.rows[0].exists) {
            console.log('[Verify] ERROR: Table "workflows" does not exist yet. Brain might still be initializing.');
            return;
        }

        const res = await client.query(`
      SELECT * FROM workflows 
      WHERE data->>'initiator' = 'gmail-gateway' 
      ORDER BY created_at DESC 
      LIMIT 10
    `);

        console.log(`[Verify] Found ${res.rowCount} workflows from Gmail Gateway.`);

        if (res.rowCount > 0) {
            res.rows.forEach(row => {
                console.log(`- Workflow ${row.id}: ${JSON.stringify(row.data).substring(0, 100)}...`);
            });
            console.log('[Verify] SUCCESS: Gateway is feeding Brain.');
        } else {
            console.log('[Verify] WARNING: No workflows found yet. Gateway might require more time or inbox is empty.');
        }

    } catch (err) {
        console.error('[Verify] Error:', err.message);
    } finally {
        await client.end();
    }
}

verifyEars();

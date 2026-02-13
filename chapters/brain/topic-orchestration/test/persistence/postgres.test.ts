import { test } from 'node:test';
import assert from 'node:assert';
import { PostgresWorkflowRepository } from '../../src/persistence/postgres';
import { Pool } from 'pg';

const DB_URL = process.env.DB_URL || 'postgresql://admin:password@localhost:5432/email_systems';

// Helper to init DB
async function initDb() {
    const pool = new Pool({ connectionString: DB_URL });
    try {
        await pool.query(`
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                current_step_id TEXT NOT NULL,
                data JSONB NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL
            );
        `);
    } catch (e) {
        console.log('Skipping Postgres tests (DB not reachable)');
        return false;
    } finally {
        await pool.end();
    }
    return true;
}

test('PostgresRepository: Save and Load', async (t) => {
    const dbAvailable = await initDb();
    if (!dbAvailable) return;

    const repo = new PostgresWorkflowRepository(DB_URL);
    const id = 'test-wf-' + Date.now();

    const state = {
        workflow_id: id,
        status: 'running' as const,
        current_step_id: 'step-1',
        data: { foo: 'bar' },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    await repo.save(state);

    const loaded = await repo.load(id);
    assert.deepStrictEqual(loaded?.workflow_id, state.workflow_id);
    assert.deepStrictEqual(loaded?.data, state.data);

    await repo.close();
});

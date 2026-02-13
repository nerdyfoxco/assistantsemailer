import { Pool } from 'pg';
import { WorkflowRepository, WorkflowState } from './repository';

export class PostgresWorkflowRepository implements WorkflowRepository {
    private pool: Pool;

    constructor(connectionString: string) {
        this.pool = new Pool({ connectionString });
    }

    async init(): Promise<void> {
        const client = await this.pool.connect();
        try {
            await client.query(`
                CREATE TABLE IF NOT EXISTS workflows (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    current_step_id TEXT,
                    data JSONB,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                );
            `);
            console.log('[Postgres] Workflows table initialized.');
        } finally {
            client.release();
        }
    }

    async save(state: WorkflowState): Promise<void> {
        const client = await this.pool.connect();
        try {
            await client.query(`
                INSERT INTO workflows (id, status, current_step_id, data, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (id) DO UPDATE SET
                  status = EXCLUDED.status,
                  current_step_id = EXCLUDED.current_step_id,
                  data = EXCLUDED.data,
                  updated_at = EXCLUDED.updated_at
            `, [
                state.workflow_id,
                state.status,
                state.current_step_id,
                state.data, // pg handles JSONB automatically, no stringify needed if type is correct, but safer to match usage
                state.created_at,
                state.updated_at
            ]);
        } finally {
            client.release();
        }
    }

    async load(workflowId: string): Promise<WorkflowState | null> {
        const client = await this.pool.connect();
        try {
            const res = await client.query('SELECT * FROM workflows WHERE id = $1', [workflowId]);
            if (res.rows.length === 0) return null;

            const row = res.rows[0];
            return {
                workflow_id: row.id,
                status: row.status,
                current_step_id: row.current_step_id,
                data: row.data, // pg automatically parses JSON
                created_at: row.created_at.toISOString(),
                updated_at: row.updated_at.toISOString()
            };
        } finally {
            client.release();
        }
    }

    async close(): Promise<void> {
        await this.pool.end();
    }
}

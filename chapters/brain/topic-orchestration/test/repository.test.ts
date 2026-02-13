import { test } from 'node:test';
import assert from 'node:assert';
import { InMemoryWorkflowRepository, WorkflowState } from '../src/persistence/repository';

test('InMemoryWorkflowRepository saves and loads state', async () => {
    const repo = new InMemoryWorkflowRepository();
    const state: WorkflowState = {
        workflow_id: 'wf-1',
        status: 'running',
        current_step_id: 'step-1',
        data: { foo: 'bar' },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    await repo.save(state);
    const loaded = await repo.load('wf-1');

    assert.deepStrictEqual(loaded, state);
});

test('InMemoryWorkflowRepository returns null for missing key', async () => {
    const repo = new InMemoryWorkflowRepository();
    const loaded = await repo.load('missing');
    assert.strictEqual(loaded, null);
});

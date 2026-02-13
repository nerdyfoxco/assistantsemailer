import { test } from 'node:test';
import assert from 'node:assert';
import { EventEmitter } from 'events';
import { OrchestratorEngine } from '../src/engine';
import { WorkflowStartedEvent, StepCompletedEvent } from '../src/events/types';
import { WorkflowState } from '../src/persistence/repository';

// Mocks
class MockStarter extends EventEmitter {
    on(event: 'startOrchestration', listener: (e: any) => void): this {
        return super.on(event, listener);
    }
}
class MockScheduler {
    public scheduledEvents: any[] = [];
    scheduleStep(correlationId: string, data: any) {
        this.scheduledEvents.push({ correlationId, data });
        return {} as any;
    }
}
class MockConsumer extends EventEmitter {
    on(event: 'stepCompleted', listener: (e: any) => void): this {
        return super.on(event, listener);
    }
}
class MockRepository {
    public storage = new Map<string, WorkflowState>();
    async save(state: WorkflowState) {
        this.storage.set(state.workflow_id, state);
    }
    async load(id: string) {
        return this.storage.get(id) || null;
    }
}

test('OrchestratorEngine persists state on start', async () => {
    const starter = new MockStarter() as any;
    const scheduler = new MockScheduler() as any;
    const consumer = new MockConsumer() as any;
    const repo = new MockRepository() as any;

    new OrchestratorEngine(starter, scheduler, consumer, repo);

    const startEvent: WorkflowStartedEvent = {
        meta: {
            event_id: '1', timestamp_utc: 'now', correlation_id: 'abc', producer: 'api', schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-1', workflow_name: 'test', initiator: 'user'
        }
    };

    await starter.emit('startOrchestration', startEvent);

    // Allow async save to complete (event emitter is sync, but onWorkflowStarted is async)
    await new Promise(r => setImmediate(r));

    const state = await repo.load('wf-1');
    assert.ok(state, 'State should be saved');
    assert.strictEqual(state.status, 'running');

    // Also verify schedule
    assert.strictEqual(scheduler.scheduledEvents.length, 1);
});

test('OrchestratorEngine updates state on completion', async () => {
    const starter = new MockStarter() as any;
    const scheduler = new MockScheduler() as any;
    const consumer = new MockConsumer() as any;
    const repo = new MockRepository() as any;

    new OrchestratorEngine(starter, scheduler, consumer, repo);

    // Pre-seed state
    await repo.save({
        workflow_id: 'wf-2',
        status: 'running',
        created_at: 'now',
        updated_at: 'now',
        data: {}
    });

    const completeEvent: StepCompletedEvent = {
        meta: {
            event_id: '2', timestamp_utc: 'now', correlation_id: 'abc', producer: 'legs', schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-2',
            step_id: 'step-1',
            step_name: 'test-step',
            status: 'success',
            outputs: { result: 'ok' }
        }
    };

    await consumer.emit('stepCompleted', completeEvent);
    await new Promise(r => setImmediate(r));

    const state = await repo.load('wf-2');
    assert.strictEqual(state.status, 'completed');
    assert.deepStrictEqual(state.data.outputs, { result: 'ok' });
});

import { test } from 'node:test';
import assert from 'node:assert';
import { WorkerDispatcher } from '../src/executor/dispatcher';
import { StepHandler, StepContext } from '../src/executor/types';

class MockHandler implements StepHandler {
    type = 'mock.echo';
    async handle(inputs: Record<string, unknown>, context: StepContext) {
        return { ...inputs, processed: true };
    }
}

test('Dispatcher executes registered handler', async () => {
    const dispatcher = new WorkerDispatcher();
    dispatcher.register(new MockHandler());

    const result = await dispatcher.dispatch('mock.echo', { foo: 'bar' }, {
        workflow_id: 'wf-1', step_id: 'step-1', correlation_id: 'corr-1'
    });

    assert.deepStrictEqual(result, { foo: 'bar', processed: true });
});

test('Dispatcher throws for unknown handler', async () => {
    const dispatcher = new WorkerDispatcher();

    await assert.rejects(async () => {
        await dispatcher.dispatch('unknown', {}, {
            workflow_id: 'wf-1', step_id: 'step-1', correlation_id: 'corr-1'
        });
    }, /No handler registered/);
});

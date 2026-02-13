const { OrchestratorEngine } = require('../chapters/brain/topic-orchestration/dist/chapters/brain/topic-orchestration/src/engine');
const { StepScheduler } = require('../chapters/brain/topic-orchestration/dist/chapters/brain/topic-orchestration/src/events/scheduler');
const { WorkflowStartConsumer } = require('../chapters/brain/topic-orchestration/dist/chapters/brain/topic-orchestration/src/events/starter');
const { WorkflowConsumer: BrainConsumer } = require('../chapters/brain/topic-orchestration/dist/chapters/brain/topic-orchestration/src/events/consumer');

const { WorkerConsumer: LegsConsumer } = require('../chapters/legs/topic-worker-runner/dist/src/events/consumer');
const { WorkerProducer: LegsProducer } = require('../chapters/legs/topic-worker-runner/dist/src/events/producer');

// Mock Event Bus
const bus = {
    listeners: {},
    emit(topic, payload) {
        if (this.listeners[topic]) {
            this.listeners[topic].forEach(fn => fn(payload));
        }
    },
    on(topic, fn) {
        if (!this.listeners[topic]) this.listeners[topic] = [];
        this.listeners[topic].push(fn);
    }
};

async function main() {
    console.log('=== Starting E2E Verification (Clean) ===');

    // --- BRAIN SETUP ---
    const brainStarter = new WorkflowStartConsumer();
    const brainScheduler = new StepScheduler();
    const brainStepConsumer = new BrainConsumer();

    new OrchestratorEngine(brainStarter, brainScheduler, brainStepConsumer);

    bus.on('pipe.workflow.started.v1', (p) => brainStarter.handleWorkflowStarted(p));
    bus.on('pipe.workflow.step.completed.v1', (p) => brainStepConsumer.handleStepCompleted(p));

    brainScheduler.on('pipe.step.scheduled.v1', (p) => {
        bus.emit('pipe.step.scheduled.v1', p);
    });

    // --- LEGS SETUP ---
    const legsConsumer = new LegsConsumer();
    const legsProducer = new LegsProducer();

    bus.on('pipe.step.scheduled.v1', (p) => legsConsumer.handleStepScheduled(p));

    legsConsumer.on('executeStep', async (event) => {
        // Simulate work
        await new Promise(r => setTimeout(r, 50));

        try {
            legsProducer.emitStepCompleted(event.meta.correlation_id, {
                workflow_id: event.data.workflow_id,
                step_id: event.data.step_id,
                step_name: event.data.step_name || 'unknown',
                status: 'success',
                outputs: { result: 'done' }
            });
        } catch (err) {
            console.error('Error in worker execution:', err);
        }
    });

    legsProducer.on('pipe.workflow.step.completed.v1', (p) => {
        bus.emit('pipe.workflow.step.completed.v1', p);
    });

    // --- TRIGGER ---
    bus.emit('pipe.workflow.started.v1', {
        meta: {
            event_id: 'e2e-start-1',
            timestamp_utc: new Date().toISOString(),
            correlation_id: 'e2e-corr-1',
            producer: 'e2e-test',
            schema_version: '1.0.0'
        },
        data: {
            workflow_id: 'wf-e2e',
            workflow_name: 'test-flow',
            initiator: 'admin'
        }
    });

    // Wait for completion
    await new Promise(r => setTimeout(r, 1000));
    console.log('=== E2E Verification Finished ===');
}

main().catch(console.error);

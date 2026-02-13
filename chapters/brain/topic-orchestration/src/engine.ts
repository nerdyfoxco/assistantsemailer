import { WorkflowStartConsumer } from './events/starter';
import { StepScheduler } from './events/scheduler';
import { WorkflowConsumer } from './events/consumer';
import { WorkflowStartedEvent, StepCompletedEvent } from './events/types';
import { WorkflowRepository } from './persistence/repository';

export class OrchestratorEngine {
    constructor(
        private starter: WorkflowStartConsumer,
        private scheduler: StepScheduler,
        private stepConsumer: WorkflowConsumer,
        private repository: WorkflowRepository
    ) {
        this.bindEvents();
    }

    private bindEvents() {
        this.starter.on('startOrchestration', (event) => this.onWorkflowStarted(event));
        this.stepConsumer.on('stepCompleted', (event) => this.onStepCompleted(event));
    }

    private async onWorkflowStarted(event: WorkflowStartedEvent) {
        console.log(`[Engine] Workflow started: ${event.data.workflow_id}`);

        // Persist Initial State
        await this.repository.save({
            workflow_id: event.data.workflow_id,
            status: 'running',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            current_step_id: 'step-1',
            data: {
                initiator: event.data.initiator,
                inputs: event.data.inputs || {}
            }
        });

        // Simple Logic: Immediately schedule Step 1
        const stepType = (event.data.inputs && typeof event.data.inputs['step_type'] === 'string')
            ? event.data.inputs['step_type']
            : 'function';

        this.scheduler.scheduleStep(event.meta.correlation_id, {
            workflow_id: event.data.workflow_id,
            step_id: 'step-1',
            step_type: stepType,
            step_name: 'initial-step',
            inputs: event.data.inputs || {}
        });
    }

    private async onStepCompleted(event: StepCompletedEvent) {
        console.log(`[Engine] Step completed: ${event.data.step_id} (${event.data.status})`);

        // Load State
        const state = await this.repository.load(event.data.workflow_id);
        if (state) {
            state.updated_at = new Date().toISOString();
            state.current_step_id = event.data.step_id;

            if (event.data.status === 'failure') {
                state.status = 'failed';
            } else {
                // In a real state machine, we'd check if this was the last step
                state.status = 'completed';
            }

            // Merge outputs into data
            if (event.data.outputs) {
                state.data = { ...state.data, outputs: event.data.outputs };
            }

            await this.repository.save(state);
        } else {
            console.warn(`[Engine] Warning: Received completion for unknown workflow ${event.data.workflow_id}`);
        }
    }
}

import * as http from 'http';
import { createRoutes } from './routes';
import { WorkflowStartConsumer } from './events/starter';
import { StepScheduler } from './events/scheduler';
import { WorkflowConsumer } from './events/consumer';
import { OrchestratorEngine } from './engine';
import { PostgresWorkflowRepository } from './persistence/postgres';

export async function startServer(config: { port: number }): Promise<{ close: () => Promise<void> }> {
    // Instantiate Logic
    const starter = new WorkflowStartConsumer();
    const scheduler = new StepScheduler();
    const consumer = new WorkflowConsumer();

    // Inject Repository
    const dbUrl = process.env.DB_URL || 'postgresql://admin:password@localhost:5432/email_systems';
    const repository = new PostgresWorkflowRepository(dbUrl);

    // Initialize DB Schema
    await repository.init();

    const engine = new OrchestratorEngine(starter, scheduler, consumer, repository);

    // Wire Scheduler mainly for logging (in real sys, would pipe to queue)
    scheduler.on('pipe.step.scheduled.v1', (event) => {
        console.log(`[Orchestrator] Emitted step.scheduled: ${event.data.step_id}`);
        // In real system: rabbitmqProducer.send(...)
    });

    const requestHandler = createRoutes(starter);
    const server = http.createServer(requestHandler);

    return new Promise((resolve) => {
        server.listen(config.port, () => {
            resolve({
                close: () => new Promise((closeResolve, closeReject) => {
                    server.close((err) => {
                        if (err) closeReject(err);
                        else closeResolve();
                    });
                }),
            });
        });
    });
}

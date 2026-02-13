import * as http from 'http';
import { createRoutes } from './routes';
import { WorkerConsumer } from './events/consumer';
import { WorkerProducer } from './events/producer';
import { WorkerDispatcher } from './executor/dispatcher';
import { MathHandler } from './handlers/math';
import { HttpHandler } from './handlers/http';

export async function startServer(config: { port: number }): Promise<{ close: () => Promise<void> }> {
    // Instantiate Logic
    const dispatcher = new WorkerDispatcher();
    dispatcher.register(new MathHandler());
    dispatcher.register(new HttpHandler());

    const consumer = new WorkerConsumer(dispatcher);
    const producer = new WorkerProducer();

    // Wire Worker Logic
    consumer.on('stepExecuted', async ({ event, outputs, status }) => {
        console.log(`[Worker] Finished ${event.data.step_id} with ${status}`);
        producer.emitStepCompleted(event.meta.correlation_id, {
            workflow_id: event.data.workflow_id,
            step_id: event.data.step_id,
            step_name: event.data.step_name || 'unknown-step', // Fallback
            status: status,
            outputs: outputs
        });
    });

    const requestHandler = createRoutes(consumer);
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

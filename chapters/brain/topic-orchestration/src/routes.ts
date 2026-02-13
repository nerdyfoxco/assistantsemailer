import * as http from 'http';
import { WorkflowStartConsumer } from './events/starter';
import { WorkflowStartedEvent } from './events/types';

export function createRoutes(consumer: WorkflowStartConsumer) {
    return (req: http.IncomingMessage, res: http.ServerResponse) => {
        if (req.method === 'GET' && req.url === '/healthz') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'ok', service: 'brain-orchestration' }));
            return;
        }

        if (req.method === 'POST' && req.url === '/v1/workflow/start') {
            let body = '';
            req.on('data', chunk => body += chunk);
            req.on('end', () => {
                try {
                    const payload = JSON.parse(body) as WorkflowStartedEvent;
                    // Security/Validation should happen here (or in consumer)
                    consumer.handleWorkflowStarted(payload);
                    res.writeHead(202, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'accepted', correlation_id: payload.meta.correlation_id }));
                } catch (err: any) {
                    console.error(err);
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: err.message }));
                }
            });
            return;
        }

        res.writeHead(404);
        res.end();
    };
}

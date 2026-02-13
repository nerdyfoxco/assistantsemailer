import * as https from 'https';
import * as http from 'http';
import { URL } from 'url';
import { StepHandler, StepContext } from '../executor/types';

export class HttpHandler implements StepHandler {
    public type = 'http.request';

    public async handle(inputs: Record<string, unknown>, context: StepContext): Promise<Record<string, unknown>> {
        const urlStr = inputs['url'];
        if (typeof urlStr !== 'string') throw new Error(`HttpHandler requires 'url' string`);

        const method = (inputs['method'] as string) || 'GET';
        const bodyInfo = inputs['body'];

        const url = new URL(urlStr);
        const lib = url.protocol === 'https:' ? https : http;

        console.log(`[HttpHandler] ${method} ${urlStr} (Step: ${context.step_id})`);

        return new Promise((resolve, reject) => {
            const req = lib.request(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'AssistantsCo-Legs/1.0'
                }
            }, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    resolve({
                        status: res.statusCode,
                        body: data
                    });
                });
            });

            req.on('error', (err) => reject(err));

            if (bodyInfo) {
                req.write(JSON.stringify(bodyInfo));
            }
            req.end();
        });
    }
}

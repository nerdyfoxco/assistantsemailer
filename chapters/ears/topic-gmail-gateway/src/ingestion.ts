import axios from 'axios';
import { GmailPoller, EmailMessage } from './client';
import { randomUUID } from 'crypto';

interface BrainConfig {
    brainUrl: string;
}

export class IngestionService {
    constructor(
        private poller: GmailPoller,
        private config: BrainConfig
    ) { }

    async startLoop(intervalMs: number = 10000) {
        console.log('[Ingestion] Starting poll loop...');
        setInterval(() => this.poll(), intervalMs);
        // Initial run
        await this.poll();
    }

    private async poll() {
        try {
            console.log('[Ingestion] Checking inbox...');
            const messages = await this.poller.checkInbox(5); // Fetch top 5
            console.log(`[Ingestion] Found ${messages.length} messages.`);

            for (const msg of messages) {
                await this.processMessage(msg);
            }
        } catch (error) {
            console.error('[Ingestion] Poll failed:', error);
        }
    }

    private async processMessage(msg: EmailMessage) {
        // Basic Deduplication: In production, we'd check if 'msg.id' was already processed.
        // For now, we assume standard "workflow.started" idempotency logic in Brain or ignore dupes.

        // Convert to Event
        const event = {
            meta: {
                event_id: randomUUID(),
                timestamp_utc: new Date().toISOString(),
                correlation_id: msg.threadId, // Use ThreadID as correlation
                producer: 'ears-gmail-gateway',
                schema_version: '1.0.0'
            },
            data: {
                workflow_id: `email-${msg.id}`,
                initiator: 'gmail-gateway',
                inputs: {
                    step_type: 'function', // Default to generic, Brain can route based on content
                    email_id: msg.id,
                    thread_id: msg.threadId,
                    snippet: msg.snippet,
                    internal_date: msg.internalDate
                    // In real world: We would parse Body/Payload here.
                }
            }
        };

        try {
            console.log(`[Ingestion] Sending workflow start for email ${msg.id}...`);
            await axios.post(`${this.config.brainUrl}/v1/workflow/start`, event);
            console.log(`[Ingestion] Successfully triggered workflow for ${msg.id}`);
        } catch (error: any) {
            console.error(`[Ingestion] Failed to trigger workflow for ${msg.id}:`, error.message);
        }
    }
}

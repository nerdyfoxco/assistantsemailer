import { google, gmail_v1 } from 'googleapis';
import { OAuth2Client } from 'google-auth-library';

export interface EmailMessage {
    id: string;
    threadId: string;
    snippet: string;
    historyId: string;
    internalDate: string;
    payload?: gmail_v1.Schema$MessagePart;
}

export class GmailPoller {
    private gmail: gmail_v1.Gmail;

    constructor(auth: OAuth2Client) {
        this.gmail = google.gmail({ version: 'v1', auth });
    }

    async checkInbox(maxResults = 10): Promise<EmailMessage[]> {
        try {
            const res = await this.gmail.users.messages.list({
                userId: 'me',
                maxResults,
                q: 'label:inbox' // Basic filter
            });

            const messages = res.data.messages || [];
            const fullMessages: EmailMessage[] = [];

            for (const msg of messages) {
                if (msg.id) {
                    const detail = await this.gmail.users.messages.get({
                        userId: 'me',
                        id: msg.id,
                        format: 'full'
                    });

                    if (detail.data.id && detail.data.threadId) {
                        fullMessages.push({
                            id: detail.data.id,
                            threadId: detail.data.threadId,
                            snippet: detail.data.snippet || '',
                            historyId: detail.data.historyId || '',
                            internalDate: detail.data.internalDate || '',
                            payload: detail.data.payload
                        });
                    }
                }
            }

            return fullMessages;
        } catch (error) {
            console.error('[GmailPoller] Error checking inbox:', error);
            throw error;
        }
    }
}

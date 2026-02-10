import { fetchEventSource } from '@microsoft/fetch-event-source';
// Let's use relative path to be safe if alias is flaky.
import { api } from '../../lib/api';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface TriageResult {
    id: string; // The thread ID usually (for list key)
    message_id: string; // The specific message ID to fetch body
    subject: string;
    sender: string;
    received_at: string;
    confidence_band: 'HIGH' | 'MEDIUM' | 'LOW';
    confidence_score: number;
    suggested_state: string;
    tags: string[];
    is_vip: boolean;
    snippet: string;
}

export interface Attachment {
    filename: string;
    mime_type: string;
    size: number;
    attachment_id: string;
}

export interface ProxyResult {
    id: string;
    snippet: string;
    html: string;
    mime_type: string;
    attachments: Attachment[];
}

export const intelligenceService = {
    // 1. Stream Work Items (Via SSE) -> UMP-50-01 + UMP-50-02
    streamWorkItems: (
        onMessage: (item: TriageResult) => void,
        onError: (err: any) => void,
        onClose: () => void
    ) => {
        // We use fetchEventSource to handle SSE robustly (reconnects, headers)
        const controller = new AbortController();

        // Get token from storage manually since fetchEventSource doesn't use axios interceptors
        const token = localStorage.getItem('token');

        fetchEventSource(`${API_URL}/intelligence/stream?limit=10`, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            signal: controller.signal,
            onmessage(msg) {
                // Determine if it's data or error
                try {
                    const data = JSON.parse(msg.data);
                    if (data.type === 'connected') {
                        console.log("Stream Connected");
                    } else if (data.type === 'error') {
                        onError(data.message);
                    } else {
                        // It's a WorkItem (TriageResult)
                        onMessage(data);
                    }
                } catch (e) {
                    console.error("Failed to parse SSE message", e);
                }
            },
            onerror(err) {
                onError(err);
                // By default it retries. If we want to stop on 401:
                if (err.status === 401) {
                    controller.abort(); // Fatal error
                    // Maybe redirect to login?
                }
            },
            onclose() {
                onClose();
            }
        });

        return () => controller.abort(); // Cleanup function
    },

    // 2. Fetch Live Body (Via Proxy) -> UMP-50-03
    getMessageBody: async (messageId: string): Promise<ProxyResult> => {
        const response = await api.get<ProxyResult>(`/intelligence/body/${messageId}`);
        return response.data;
    }
};

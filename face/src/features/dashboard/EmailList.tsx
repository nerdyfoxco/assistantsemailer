import { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { format } from 'date-fns';
import { Loader2, RefreshCw, Mail } from 'lucide-react';
import { cn } from '../../lib/utils';

interface Email {
    id: string;
    subject: string;
    from: string;
    snippet: string;
    received_at: string;
    gmail_id: string;
}

export function EmailList() {
    const [emails, setEmails] = useState<Email[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isSyncing, setIsSyncing] = useState(false);

    const fetchEmails = async () => {
        setIsLoading(true);
        try {
            const response = await api.get('/emails/');
            setEmails(response);
        } catch (error) {
            console.error("Failed to fetch emails", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSync = async () => {
        setIsSyncing(true);
        try {
            await api.post('/emails/sync');
            await fetchEmails();
        } catch (error) {
            console.error("Sync failed", error);
        } finally {
            setIsSyncing(false);
        }
    };

    useEffect(() => {
        fetchEmails();
    }, []);

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium">Recent Emails</h3>
                <button
                    onClick={handleSync}
                    disabled={isSyncing}
                    className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2"
                >
                    <RefreshCw className={cn("mr-2 h-4 w-4", isSyncing && "animate-spin")} />
                    Sync
                </button>
            </div>

            <div className="rounded-md border">
                {isLoading && emails.length === 0 ? (
                    <div className="p-8 text-center text-muted-foreground">
                        <Loader2 className="mx-auto h-8 w-8 animate-spin" />
                        <p className="mt-2">Loading emails...</p>
                    </div>
                ) : emails.length === 0 ? (
                    <div className="p-8 text-center text-muted-foreground">
                        <Mail className="mx-auto h-8 w-8 opacity-50" />
                        <p className="mt-2">No emails found. Click Sync to fetch from Gmail.</p>
                    </div>
                ) : (
                    <div className="divide-y">
                        {emails.map((email) => (
                            <div key={email.id} className="p-4 hover:bg-muted/50 transition-colors">
                                <div className="flex items-start justify-between gap-4">
                                    <div className="grid gap-1">
                                        <div className="font-semibold">{email.subject}</div>
                                        <div className="text-sm font-medium text-muted-foreground">{email.from}</div>
                                        <div className="text-sm text-muted-foreground line-clamp-2">{email.snippet}</div>
                                    </div>
                                    <div className="text-xs text-muted-foreground whitespace-nowrap">
                                        {format(new Date(email.received_at), 'MMM d, h:mm a')}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../lib/api';
import { Loader2 } from 'lucide-react';

export function GoogleCallbackPage() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState("Processing Google Login...");
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const code = searchParams.get('code');
        const googleTokens = searchParams.get('google_tokens');

        if (googleTokens) {
            // Case 2: Backend Redirected with Tokens (Server-Side Flow)
            // We now have tokens, but need to link them to the current user via API
            const linkAccount = async () => {
                try {
                    setStatus("Linking Google Account...");
                    // We send the JSON string as is
                    await api.post('/auth/google/connect', { tokens: googleTokens });
                    setStatus("Connected! Redirecting...");
                    setTimeout(() => navigate('/dashboard'), 1000);
                } catch (err: any) {
                    console.error("Link Failed:", err);
                    setError(err.response?.data?.detail || "Failed to link account.");
                }
            };
            linkAccount();
            return;
        }

        if (code) {
            // Case 1: Direct Callback (Client-Side Flow - Deprecated by new config but keeping for safety)
            setError("Received Auth Code but expected Tokens via Backend Redirect. Config mismatch?");
            return;
        }

        setError("No artifacts received.");

    }, [searchParams, navigate]);

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-neutral-50 p-4">
                <div className="bg-white p-6 rounded-lg shadow-sm border border-red-200 max-w-md w-full text-center">
                    <h2 className="text-xl font-bold text-red-600 mb-2">Connection Failed</h2>
                    <p className="text-slate-600 mb-4">{error}</p>
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="px-4 py-2 bg-slate-100 hover:bg-slate-200 rounded-md text-sm font-medium"
                    >
                        Return to Dashboard
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-neutral-50">
            <Loader2 className="h-8 w-8 animate-spin text-primary mb-4" />
            <p className="text-slate-600 font-medium">{status}</p>
        </div>
    );
}

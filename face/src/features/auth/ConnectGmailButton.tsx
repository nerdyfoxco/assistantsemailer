import { useState } from 'react';
import { api } from '../../lib/api';
import { Loader2, Mail } from 'lucide-react';

export function ConnectGmailButton() {
    const [isLoading, setIsLoading] = useState(false);

    const handleConnect = async () => {
        setIsLoading(true);
        try {
            // 1. Get the Google Auth URL from Backend
            const response = await api.get('/auth/google/login');
            const { url } = response.data;

            // 2. Redirect the user
            window.location.href = url;
        } catch (error) {
            console.error("Failed to initiate Google Login:", error);
            alert("Failed to connect to Google. See console.");
            setIsLoading(false);
        }
    };

    return (
        <button
            onClick={handleConnect}
            disabled={isLoading}
            className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-white text-slate-900 shadow-sm border border-slate-200 hover:bg-slate-100 h-9 px-4 py-2"
        >
            {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Mail className="mr-2 h-4 w-4" />}
            Connect Gmail
        </button>
    );
}

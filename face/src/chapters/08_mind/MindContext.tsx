
import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import { api } from '../../lib/api';
import type { Decision } from '../../lib/api';

// Types (should ideally generally be in a shared type file, but here for now)
export type ActionType = 'REPLY' | 'ARCHIVE' | 'IGNORE' | 'ESCALATE';

interface MindContextType {
    isThinking: boolean;
    decision: Decision | null;
    error: string | null;
    analyzeEmail: (messageId: string) => Promise<void>;
    executeDecision: (messageId: string, decision: Decision) => Promise<void>;
    clearDecision: () => void;
}

const MindContext = createContext<MindContextType | undefined>(undefined);

export const useMind = () => {
    const context = useContext(MindContext);
    if (!context) {
        throw new Error('useMind must be used within a MindProvider');
    }
    return context;
};

export const MindProvider = ({ children }: { children: ReactNode }) => {
    const [isThinking, setIsThinking] = useState(false);
    const [decision, setDecision] = useState<Decision | null>(null);
    const [error, setError] = useState<string | null>(null);

    const analyzeEmail = async (messageId: string) => {
        setIsThinking(true);
        setError(null);
        setDecision(null);
        try {
            // Call the Backend API
            const response = await api.post<Decision>(`/mind/think/${messageId}`);
            setDecision(response.data);
        } catch (err: any) {
            console.error("Analysis failed:", err);
            setError(err.response?.data?.detail || "Failed to analyze email");
        } finally {
            setIsThinking(false);
        }
    };

    const executeDecision = async (messageId: string, decision: Decision) => {
        setIsThinking(true); // Re-use thinking state for execution
        try {
            await api.post('/mind/execute', {
                message_id: messageId,
                decision: decision
            });
            // Clear decision on success? Or keep it to show "Done"?
            // Let's clear it for now to reset UI
            setDecision(null);
        } catch (err: any) {
            console.error("Execution failed:", err);
            setError(err.response?.data?.detail || "Failed to execute decision");
        } finally {
            setIsThinking(false);
        }
    };

    const clearDecision = () => {
        setDecision(null);
        setError(null);
    };

    return (
        <MindContext.Provider value={{
            isThinking,
            decision,
            error,
            analyzeEmail,
            executeDecision,
            clearDecision
        }}>
            {children}
        </MindContext.Provider>
    );
};

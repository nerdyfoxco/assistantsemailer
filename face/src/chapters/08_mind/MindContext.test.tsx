
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { MindProvider, useMind, Decision } from './MindContext';
import { api } from '../../lib/api';
import React, { ReactNode } from 'react';

// Mock API
vi.mock('../../lib/api', () => ({
    api: {
        post: vi.fn()
    }
}));

const wrapper = ({ children }: { children: ReactNode }) => (
    <MindProvider>{children}</MindProvider>
);

describe('MindContext', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should initialize with default values', () => {
        const { result } = renderHook(() => useMind(), { wrapper });
        expect(result.current.isThinking).toBe(false);
        expect(result.current.decision).toBeNull();
        expect(result.current.error).toBeNull();
    });

    it('analyzeEmail should call API and update state', async () => {
        const mockDecision: Decision = {
            action: 'REPLY',
            reasoning: 'Test reasoning',
            tags: ['test']
        };
        (api.post as any).mockResolvedValueOnce({ data: mockDecision });

        const { result } = renderHook(() => useMind(), { wrapper });

        // Initial state
        expect(result.current.isThinking).toBe(false);

        // Trigger action
        let promise;
        act(() => {
            promise = result.current.analyzeEmail('123');
        });

        // Check loading state (optimistic)
        expect(result.current.isThinking).toBe(true);

        await act(async () => {
            await promise;
        });

        // Check final state
        expect(result.current.isThinking).toBe(false);
        expect(result.current.decision).toEqual(mockDecision);
        expect(api.post).toHaveBeenCalledWith('/mind/think/123');
    });

    it('analyzeEmail should handle errors', async () => {
        const errorMsg = 'API Error';
        (api.post as any).mockRejectedValueOnce({
            response: { data: { detail: errorMsg } }
        });

        const { result } = renderHook(() => useMind(), { wrapper });

        await act(async () => {
            await result.current.analyzeEmail('123');
        });

        expect(result.current.isThinking).toBe(false);
        expect(result.current.decision).toBeNull();
        expect(result.current.error).toBe(errorMsg);
    });
});

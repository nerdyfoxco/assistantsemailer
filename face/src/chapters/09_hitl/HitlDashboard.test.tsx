
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { HitlDashboard } from './HitlDashboard';
import { hitl } from '../../lib/api';
import React from 'react';

// Mock API
vi.mock('../../lib/api', () => ({
    hitl: {
        getQueue: vi.fn(),
        claimRequest: vi.fn(),
        resolveRequest: vi.fn()
    },
    api: {
        get: vi.fn(),
        post: vi.fn(),
        interceptors: {
            request: { use: vi.fn() },
            response: { use: vi.fn() }
        }
    }
}));

// Mock ResolutionCard to avoid complexity
vi.mock('./ResolutionCard', () => ({
    ResolutionCard: ({ onComplete }: any) => (
        <div data-testid="resolution-card">
            Resolution Card
            <button onClick={onComplete}>Complete</button>
        </div>
    )
}));

describe('HitlDashboard', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders loading state initially', () => {
        (hitl.getQueue as any).mockReturnValue(new Promise(() => { })); // Never resolves
        render(<HitlDashboard />);
        const button = screen.getByRole('button');
        expect(button).toBeDisabled();
        // expect(screen.queryByText('Refresh')).not.toBeInTheDocument(); // Loader should be there
    });

    it('renders queue items after fetch', async () => {
        const mockQueue = [
            { id: '1', reason: 'Ambiguity', state: 'PENDING', created_at: new Date().toISOString() },
            { id: '2', reason: 'Policy', state: 'PENDING', created_at: new Date().toISOString() }
        ];
        (hitl.getQueue as any).mockResolvedValue(mockQueue);

        render(<HitlDashboard />);

        await waitFor(() => {
            expect(screen.getByText('Ambiguity')).toBeInTheDocument();
            expect(screen.getByText('Policy')).toBeInTheDocument();
        });
    });

    it('handles claiming a request', async () => {
        const mockItem = { id: '1', reason: 'Ambiguity', state: 'PENDING', created_at: new Date().toISOString() };
        (hitl.getQueue as any).mockResolvedValue([mockItem]);
        (hitl.claimRequest as any).mockResolvedValue({});

        render(<HitlDashboard />);

        await waitFor(() => screen.getByText('Ambiguity'));

        fireEvent.click(screen.getByText('Ambiguity'));

        await waitFor(() => {
            expect(hitl.claimRequest).toHaveBeenCalledWith('1', 'agent-007');
        });
    });
});

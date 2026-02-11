
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DecisionCard } from './DecisionCard';
import { useMind } from './MindContext';


// Mock useMind
vi.mock('./MindContext', () => ({
    useMind: vi.fn(),
}));

describe('DecisionCard', () => {
    const mockAnalyze = vi.fn();
    const mockExecute = vi.fn();
    const mockClear = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders "Ask Strategist" button when no decision', () => {
        (useMind as any).mockReturnValue({
            decision: null,
            isThinking: false,
            error: null,
            analyzeEmail: mockAnalyze,
            executeDecision: mockExecute,
            clearDecision: mockClear,
        });

        render(<DecisionCard messageId="123" />);
        expect(screen.getByText('Ask Strategist')).toBeDefined();

        fireEvent.click(screen.getByText('Ask Strategist'));
        expect(mockAnalyze).toHaveBeenCalledWith('123');
    });

    it('renders loading state', () => {
        (useMind as any).mockReturnValue({
            decision: null,
            isThinking: true,
            error: null,
            analyzeEmail: mockAnalyze,
            executeDecision: mockExecute,
            clearDecision: mockClear,
        });

        render(<DecisionCard messageId="123" />);
        expect(screen.getByText('Strategist is thinking...')).toBeDefined();
    });

    it('renders decision', () => {
        const mockDecision = {
            action: 'REPLY',
            reasoning: 'Because I said so',
            tags: ['urgent'],
            draft_body: 'Hello world'
        };

        (useMind as any).mockReturnValue({
            decision: mockDecision,
            isThinking: false,
            error: null,
            analyzeEmail: mockAnalyze,
            executeDecision: mockExecute,
            clearDecision: mockClear,
        });

        render(<DecisionCard messageId="123" />);

        // Use regex for partial matching
        expect(screen.getByText(/REPLY/i)).toBeDefined();
        expect(screen.getByText(/Because I said so/i)).toBeDefined();
        expect(screen.getByText(/Hello world/i)).toBeDefined();
        expect(screen.getByText(/urgent/i)).toBeDefined();

        // Use getByRole for button
        const approveBtn = screen.getByRole('button', { name: /Approve/i });
        expect(approveBtn).toBeDefined();

        fireEvent.click(approveBtn);
        expect(mockExecute).toHaveBeenCalledWith('123', mockDecision);
    });

    it('renders error state', () => {
        (useMind as any).mockReturnValue({
            decision: null,
            isThinking: false,
            error: 'Something went wrong',
            analyzeEmail: mockAnalyze,
            executeDecision: mockExecute,
            clearDecision: mockClear,
        });

        render(<DecisionCard messageId="123" />);
        expect(screen.getByText('Error: Something went wrong')).toBeDefined();
    });
});

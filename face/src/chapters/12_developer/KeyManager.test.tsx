import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { KeyManager } from './KeyManager';
import { api } from '@/lib/api';

// Mock dependencies
vi.mock('@/lib/api', () => ({
    api: {
        get: vi.fn(),
        post: vi.fn(),
        delete: vi.fn()
    }
}));

describe('KeyManager', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders empty state correctly', async () => {
        (api.get as any).mockResolvedValueOnce({ data: [] });
        render(<KeyManager />);

        await waitFor(() => {
            expect(screen.getByText(/No API keys found/i)).toBeInTheDocument();
        });
    });

    it('renders list of keys', async () => {
        const mockKeys = [
            { id: '1', name: 'Test Key', prefix: 'sk_live_', created_at: new Date().toISOString(), scopes: [] }
        ];
        (api.get as any).mockResolvedValueOnce({ data: mockKeys });

        render(<KeyManager />);

        await waitFor(() => {
            expect(screen.getByText('Test Key')).toBeInTheDocument();
            expect(screen.getByText(/sk_live_/i)).toBeInTheDocument();
        });
    });

    it('generates a new key', async () => {
        (api.get as any).mockResolvedValueOnce({ data: [] });
        render(<KeyManager />);

        // Open Dialog
        fireEvent.click(screen.getByText(/Generate New Key/i));

        // Input Name
        const input = screen.getByPlaceholderText(/e.g. CI\/CD Pipeline/i);
        fireEvent.change(input, { target: { value: 'New Key' } });

        // Mock Generation Response
        (api.post as any).mockResolvedValueOnce({
            data: {
                id: '2',
                name: 'New Key',
                prefix: 'sk_live_',
                created_at: new Date().toISOString(),
                scopes: [],
                raw_key: 'sk_live_SECRET_VALUE'
            }
        });
        (api.get as any).mockResolvedValueOnce({ data: [{ id: '2', name: 'New Key', prefix: 'sk_live_', created_at: new Date().toISOString(), scopes: [] }] });

        // Submit
        fireEvent.click(screen.getByRole('button', { name: 'Generate Key' })); // Exact match might fail if icon is present, better use test id or specific text

        // Verify Raw Key Shown
        await waitFor(() => {
            expect(screen.getByText('sk_live_SECRET_VALUE')).toBeInTheDocument();
        });
    });
});

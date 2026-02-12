import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Onboarding } from './Onboarding';
import { BrowserRouter } from 'react-router-dom';
import { api } from '@/lib/api';
import '@testing-library/jest-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock API
vi.mock('@/lib/api', () => ({
    api: {
        post: vi.fn()
    }
}));

describe('Onboarding Component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    const renderComponent = () => {
        render(
            <BrowserRouter>
                <Onboarding />
            </BrowserRouter>
        );
    };

    it('renders the initial email step', () => {
        renderComponent();
        expect(screen.getByText(/Create your account/i)).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/name@example.com/i)).toBeInTheDocument();
        // Use getAllByRole because there might be multiple "Continue" (hidden/visible) if transitions mimic multiple items?
        // But here we just want the button that says "Continue"
        const btn = screen.getByRole('button', { name: /Continue/i });
        expect(btn).toBeInTheDocument();
    });

    it('validates email input before proceeding', () => {
        renderComponent();
        const continueBtn = screen.getByRole('button', { name: /Continue/i });
        expect(continueBtn).toBeDisabled();

        const emailInput = screen.getByPlaceholderText(/name@example.com/i);
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        expect(continueBtn).toBeEnabled();
    });

    it('transitions to details step on email submit', async () => {
        renderComponent();
        const emailInput = screen.getByPlaceholderText(/name@example.com/i);
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });


        const form = screen.getByRole('button', { name: /Continue/i }).closest('form');
        if (form) fireEvent.submit(form);

        // Wait for animation
        await waitFor(() => {
            expect(screen.getByText(/Finish setting up/i)).toBeVisible();
        });
        expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    });

    it('submits signup form successfully', async () => {
        renderComponent();
        // Step 1: Email
        const emailInput = screen.getByPlaceholderText(/name@example.com/i);
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        // Step 2: Details
        expect(await screen.findByLabelText(/Password/i)).toBeInTheDocument();
        fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'password123' } });
        fireEvent.change(screen.getByLabelText(/Workspace Name/i), { target: { value: 'Acme' } });
        fireEvent.click(screen.getByLabelText(/Terms of Service/i)); // Check TOS

        // Mock Success
        (api.post as any).mockResolvedValueOnce({ data: { user_id: '123' } });

        fireEvent.click(screen.getByRole('button', { name: /Create Account/i }));

        // Expect API call
        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith('/public/auth/signup', {
                email: 'test@example.com',
                password: 'password123',
                tenant_name: 'Acme',
                agree_tos: true
            });
        });

        // Expect Success Step
        expect(await screen.findByText(/Welcome aboard!/i)).toBeInTheDocument();
    });

    it('handles signup error', async () => {
        renderComponent();
        // Navigate to Step 2
        fireEvent.change(screen.getByPlaceholderText(/name@example.com/i), { target: { value: 'test@example.com' } });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        // Fill Form
        expect(await screen.findByLabelText(/Password/i)).toBeInTheDocument();
        fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'password123' } });
        fireEvent.change(screen.getByLabelText(/Workspace Name/i), { target: { value: 'Acme' } });
        fireEvent.click(screen.getByLabelText(/Terms of Service/i));

        // Mock Failure
        (api.post as any).mockRejectedValueOnce({
            response: { data: { detail: 'Email already exists' } }
        });

        fireEvent.click(screen.getByRole('button', { name: /Create Account/i }));

        expect(await screen.findByText(/Email already exists/i)).toBeInTheDocument();
    });
});

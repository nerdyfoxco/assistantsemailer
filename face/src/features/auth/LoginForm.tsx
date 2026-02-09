import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { api } from '../../lib/api';
import { cn } from '../../lib/utils';
import { Loader2 } from 'lucide-react';

const loginSchema = z.object({
    username: z.string().email("Invalid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

    const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
        resolver: zodResolver(loginSchema),
    });

    const onSubmit = async (data: LoginFormData) => {
        setIsLoading(true);
        setError(null);
        try {
            // Note: Backend expects generic form data for OAuth2 usually, but let's try JSON first based on our implementation
            // Or requests typically use URLSearchParams for OAuth2 password flow.
            // Let's check `auth_service.py`... 
            // Fastapi `OAuth2PasswordRequestForm` expects form-data.

            const formData = new URLSearchParams();
            formData.append('username', data.username);
            formData.append('password', data.password);

            const response = await api.post('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            const { access_token } = response.data;
            localStorage.setItem('token', access_token);
            setToken(access_token);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Login failed");
        } finally {
            setIsLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setToken(null);
    }

    if (token) {
        return (
            <div className="p-6 bg-card border rounded-lg shadow-sm text-center">
                <h2 className="text-xl font-semibold text-green-600 mb-4">Authenticated!</h2>
                <p className="text-muted-foreground mb-4">Token stored in LocalStorage.</p>
                <button
                    onClick={handleLogout}
                    className="px-4 py-2 bg-destructive text-destructive-foreground rounded-md hover:bg-destructive/90"
                >
                    Logout
                </button>
            </div>
        )
    }

    return (
        <div className="w-full max-w-sm mx-auto p-6 bg-card border rounded-lg shadow-sm">
            <h2 className="text-2xl font-bold text-center mb-6">Login</h2>

            {error && (
                <div className="p-3 mb-4 text-sm text-red-500 bg-red-50 rounded-md border border-red-200">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div className="space-y-2">
                    <label className="text-sm font-medium leading-none" htmlFor="username">Email</label>
                    <input
                        {...register("username")}
                        id="username"
                        type="email"
                        className={cn(
                            "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
                            errors.username && "border-red-500"
                        )}
                        placeholder="admin@example.com"
                    />
                    {errors.username && <p className="text-xs text-red-500">{errors.username.message}</p>}
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-medium leading-none" htmlFor="password">Password</label>
                    <input
                        {...register("password")}
                        id="password"
                        type="password"
                        className={cn(
                            "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
                            errors.password && "border-red-500"
                        )}
                    />
                    {errors.password && <p className="text-xs text-red-500">{errors.password.message}</p>}
                </div>

                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2"
                >
                    {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                    Sign In
                </button>
            </form>
        </div>
    );
}

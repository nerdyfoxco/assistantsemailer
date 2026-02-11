import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { api } from '../../lib/api';
import { cn } from '../../lib/utils';
import { Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const loginSchema = z.object({
    username: z.string().email("Invalid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const navigate = useNavigate();
    const [searchParams] = useState(new URLSearchParams(window.location.search));

    useEffect(() => {
        const urlToken = searchParams.get('token');
        if (urlToken) {
            localStorage.setItem('token', urlToken);
            setToken(urlToken);
            // navigate('/dashboard'); // Remove token from URL for cleanliness, but keep it simple
            // Force navigate to clean URL
            window.location.href = '/dashboard';
        }
    }, [searchParams, navigate]);

    const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
        resolver: zodResolver(loginSchema),
    });

    const onSubmit = async (data: LoginFormData) => {
        setIsLoading(true);
        setError(null);
        try {
            // Backend expects JSON { email, password }
            const response = await api.post('/auth/login', {
                email: data.username,
                password: data.password
            });

            const { access_token } = response.data;
            localStorage.setItem('token', access_token);
            setToken(access_token);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || "Login failed");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (token) {
            navigate('/dashboard');
        }
    }, [token, navigate]);

    if (token) return null;

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

                <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                        <span className="w-full border-t" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                        <span className="bg-card px-2 text-muted-foreground">Or continue with</span>
                    </div>
                </div>

                <button
                    type="button"
                    disabled={isLoading}
                    onClick={() => {
                        // Redirect to Backend Google Auth Endpoint
                        // WE assume backend is at http://localhost:8000
                        window.location.href = "http://localhost:8000/api/v1/auth/google/login";
                    }}
                    className="w-full inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2"
                >
                    <svg className="mr-2 h-4 w-4" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="google" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512">
                        <path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"></path>
                    </svg>
                    Google
                </button>
            </form>
        </div>
    );
}

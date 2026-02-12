
import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from 'react-router-dom';
import { Mail, Check, Loader2, ArrowRight } from "lucide-react";
import { api } from '@/lib/api';

export const Onboarding: React.FC = () => {
    // const navigate = useNavigate(); // Unused
    const [step, setStep] = useState<"email" | "details" | "success">("email");
    const [isLoading, setIsLoading] = useState(false);

    // Form State
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        tenantName: "",
        agreeTos: false
    });
    const [error, setError] = useState<string | null>(null);

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setIsLoading(true);

        try {
            await api.post('/public/auth/signup', {
                email: formData.email,
                password: formData.password,
                tenant_name: formData.tenantName,
                agree_tos: formData.agreeTos
            });
            setStep("success");
            // Auto login or redirect could happen here, for now success screen
        } catch (err: any) {
            setError(err.response?.data?.detail || "Signup failed. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background flex flex-col md:flex-row font-sans text-foreground">
            {/* Left Panel: Branding */}
            <div className="hidden md:flex flex-col justify-between w-1/3 bg-muted p-12 border-r">
                <div className="flex items-center gap-2 font-bold text-xl tracking-tighter">
                    <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center">
                        <Mail className="h-5 w-5 text-primary" />
                    </div>
                    <span>Assistants Co.</span>
                </div>
                <div className="space-y-6">
                    <blockquote className="text-lg font-medium leading-relaxed">
                        "Since switching to Assistants Co, I haven't manually triaged an email in 3 months. It's like magic."
                    </blockquote>
                    <div className="flex items-center gap-4">
                        <div className="h-10 w-10 rounded-full bg-slate-200" />
                        <div>
                            <div className="font-semibold">Sarah J.</div>
                            <div className="text-sm text-muted-foreground">CTO, TechFlow</div>
                        </div>
                    </div>
                </div>
                <div className="text-sm text-muted-foreground">
                    © 2026 Assistants Company Incorp.
                </div>
            </div>

            {/* Right Panel: Form */}
            <div className="flex-1 flex items-center justify-center p-8">
                <div className="max-w-md w-full space-y-8">

                    {step === "email" && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
                            <div className="space-y-2 text-center md:text-left">
                                <h1 className="text-3xl font-bold tracking-tight">Create your account</h1>
                                <p className="text-muted-foreground">Start your 14-day free trial. No credit card required.</p>
                            </div>

                            <div className="space-y-4">
                                <Button variant="outline" className="w-full h-11" onClick={() => window.location.href = "http://localhost:8000/auth/login"}>
                                    <svg className="mr-2 h-4 w-4" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="google" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512"><path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"></path></svg>
                                    Sign up with Google
                                </Button>
                                <div className="relative">
                                    <div className="absolute inset-0 flex items-center">
                                        <span className="w-full border-t" />
                                    </div>
                                    <div className="relative flex justify-center text-xs uppercase">
                                        <span className="bg-background px-2 text-muted-foreground">Or continue with email</span>
                                    </div>
                                </div>
                                <form onSubmit={(e) => { e.preventDefault(); setStep("details"); }} className="space-y-4">
                                    <div className="space-y-2">
                                        <Input
                                            placeholder="name@example.com"
                                            type="email"
                                            required
                                            value={formData.email}
                                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        />
                                    </div>
                                    <Button type="submit" className="w-full">Continue <ArrowRight className="ml-2 h-4 w-4" /></Button>
                                </form>
                            </div>
                        </div>
                    )}

                    {step === "details" && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
                            <div className="space-y-2">
                                <h1 className="text-3xl font-bold tracking-tight">Finish setting up</h1>
                                <p className="text-muted-foreground">Enter your details to create your workspace.</p>
                            </div>
                            <form onSubmit={handleSignup} className="space-y-4">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Password</label>
                                    <Input
                                        type="password"
                                        required
                                        value={formData.password}
                                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Workspace Name</label>
                                    <Input
                                        placeholder="Acme Corp"
                                        required
                                        value={formData.tenantName}
                                        onChange={(e) => setFormData({ ...formData, tenantName: e.target.value })}
                                    />
                                </div>
                                <div className="flex items-center space-x-2">
                                    <input
                                        type="checkbox"
                                        id="terms"
                                        required
                                        checked={formData.agreeTos}
                                        onChange={(e) => setFormData({ ...formData, agreeTos: e.target.checked })}
                                        className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                                    />
                                    <label htmlFor="terms" className="text-sm text-muted-foreground">
                                        I agree to the <Link to="/security" className="underline hover:text-primary">Terms of Service</Link> and Privacy Policy.
                                    </label>
                                </div>

                                {error && (
                                    <div className="p-3 text-sm text-red-500 bg-red-500/10 rounded-md">
                                        {error}
                                    </div>
                                )}

                                <div className="flex gap-4">
                                    <Button type="button" variant="ghost" onClick={() => setStep("email")}>Back</Button>
                                    <Button type="submit" className="flex-1" disabled={isLoading}>
                                        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                        Create Account
                                    </Button>
                                </div>
                            </form>
                        </div>
                    )}

                    {step === "success" && (
                        <div className="text-center space-y-6 animate-in zoom-in-50 duration-500">
                            <div className="mx-auto h-16 w-16 bg-green-500/10 rounded-full flex items-center justify-center">
                                <Check className="h-8 w-8 text-green-500" />
                            </div>
                            <h2 className="text-2xl font-bold">Welcome aboard!</h2>
                            <p className="text-muted-foreground">
                                Your account has been created successfully.
                            </p>
                            <Link to="/login">
                                <Button className="w-full">Sign In to Dashboard</Button>
                            </Link>
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
};

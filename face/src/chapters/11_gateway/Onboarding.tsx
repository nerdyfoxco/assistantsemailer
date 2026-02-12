import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from 'react-router-dom';
import { Mail, Check, Loader2, ArrowRight, AlertCircle } from "lucide-react";
import { api } from '@/lib/api';

export const Onboarding: React.FC = () => {
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
            // In a real app, we'd auto-login here or redirect.
            // For this phase, we show the Success state.
        } catch (err: any) {
            setError(err.response?.data?.detail || "Signup failed. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background flex flex-col md:flex-row font-sans text-foreground overflow-hidden">
            {/* Left Panel: Branding */}
            <div className="hidden md:flex flex-col justify-between w-1/3 bg-muted p-12 border-r relative overflow-hidden">
                {/* Decoration */}
                <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary/5 rounded-full blur-3xl pointer-events-none" />

                <div className="flex items-center gap-2 font-bold text-xl tracking-tighter relative z-10">
                    <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center backdrop-blur-sm">
                        <Mail className="h-5 w-5 text-primary" />
                    </div>
                    <span>Assistants Co.</span>
                </div>
                <div className="space-y-6 relative z-10">
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
                <div className="text-sm text-muted-foreground relative z-10">
                    © 2026 Assistants Company Incorp.
                </div>
            </div>

            {/* Right Panel: Form */}
            <div className="flex-1 flex items-center justify-center p-8 relative">
                <div className="max-w-md w-full relative min-h-[400px]">

                    {/* Step 1: Email */}
                    <div className={`transition-all duration-500 absolute inset-0 
                        ${step === 'email' ? 'opacity-100 translate-x-0 pointer-events-auto' : 'opacity-0 -translate-x-8 pointer-events-none'}`}>

                        <div className="space-y-6">
                            <div className="space-y-2 text-center md:text-left">
                                <h1 className="text-3xl font-bold tracking-tight">Create your account</h1>
                                <p className="text-muted-foreground">Start your 14-day free trial. No credit card required.</p>
                            </div>

                            <div className="space-y-4">
                                <Button variant="outline" className="w-full h-11 relative overflow-hidden group" onClick={() => window.location.href = "http://localhost:8000/auth/login"}>
                                    <div className="absolute inset-0 bg-slate-100 opacity-0 group-hover:opacity-100 transition-opacity" />
                                    <span className="relative flex items-center justify-center gap-2">
                                        <svg className="h-4 w-4" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="google" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512"><path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"></path></svg>
                                        Sign up with Google
                                    </span>
                                </Button>
                                <div className="relative">
                                    <div className="absolute inset-0 flex items-center">
                                        <span className="w-full border-t" />
                                    </div>
                                    <div className="relative flex justify-center text-xs uppercase">
                                        <span className="bg-background px-2 text-muted-foreground">Or continue with email</span>
                                    </div>
                                </div>
                                <form onSubmit={(e) => {
                                    e.preventDefault();
                                    if (formData.email) setStep("details");
                                }} className="space-y-4">
                                    <div className="space-y-2">
                                        <Input
                                            placeholder="name@example.com"
                                            type="email"
                                            required
                                            className="h-11"
                                            value={formData.email}
                                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        />
                                    </div>
                                    <Button type="submit" className="w-full h-11" disabled={!formData.email}>
                                        Continue <ArrowRight className="ml-2 h-4 w-4" />
                                    </Button>
                                </form>
                            </div>
                        </div>
                    </div>

                    {/* Step 2: Details */}
                    <div className={`transition-all duration-500 absolute inset-0 
                        ${step === 'details' ? 'opacity-100 translate-x-0 pointer-events-auto delay-100' : 'opacity-0 translate-x-8 pointer-events-none'}`}>

                        <div className="space-y-6">
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
                                        className="h-11"
                                        value={formData.password}
                                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Workspace Name</label>
                                    <Input
                                        placeholder="Acme Corp"
                                        required
                                        className="h-11"
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
                                    <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md flex items-center gap-2 animate-in slide-in-from-top-2">
                                        <AlertCircle className="h-4 w-4" />
                                        {error}
                                    </div>
                                )}

                                <div className="flex gap-4">
                                    <Button type="button" variant="ghost" onClick={() => setStep("email")} className="h-11">Back</Button>
                                    <Button type="submit" className="flex-1 h-11" disabled={isLoading}>
                                        {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                                        {isLoading ? 'Creating Account...' : 'Create Account'}
                                    </Button>
                                </div>
                            </form>
                        </div>
                    </div>

                    {/* Step 3: Success */}
                    <div className={`transition-all duration-500 absolute inset-0 flex items-center justify-center
                        ${step === 'success' ? 'opacity-100 scale-100 delay-200 pointer-events-auto' : 'opacity-0 scale-95 pointer-events-none'}`}>

                        <div className="text-center space-y-6 w-full">
                            <div className="mx-auto h-20 w-20 bg-green-500/10 rounded-full flex items-center justify-center animate-in zoom-in-50 duration-500">
                                <Check className="h-10 w-10 text-green-500" />
                            </div>
                            <div className="space-y-2">
                                <h2 className="text-2xl font-bold">Welcome aboard!</h2>
                                <p className="text-muted-foreground">
                                    Your account has been created successfully.
                                </p>
                            </div>
                            <Link to="/login" className="block w-full">
                                <Button className="w-full h-11">Sign In to Dashboard</Button>
                            </Link>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

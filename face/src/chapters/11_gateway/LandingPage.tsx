
import React from 'react';
import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2, Shield, Zap, Globe, Mail } from "lucide-react";
import { Link } from 'react-router-dom';

export const LandingPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-background flex flex-col font-sans text-foreground selection:bg-primary/20">
            {/* Navigation */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container flex h-16 items-center justify-between">
                    <div className="flex items-center gap-2 font-bold text-xl tracking-tighter">
                        <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center">
                            <Mail className="h-5 w-5 text-primary" />
                        </div>
                        <span>Assistants Co.</span>
                    </div>
                    <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
                        <a href="#features" className="hover:text-foreground transition-colors">Features</a>
                        <Link to="/security" className="hover:text-foreground transition-colors">Security</Link>
                        <a href="#pricing" className="hover:text-foreground transition-colors">Pricing</a>
                    </nav>
                    <div className="flex items-center gap-4">
                        <Link to="/login">
                            <Button variant="ghost" size="sm">Log in</Button>
                        </Link>
                        <Link to="/signup">
                            <Button size="sm" className="rounded-full px-6">Get Started</Button>
                        </Link>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <main className="flex-1">
                <section className="container pt-24 pb-32 md:pt-32 md:pb-48 flex flex-col items-center text-center space-y-8">
                    <div className="space-y-4 max-w-4xl mx-auto">
                        <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-primary/10 text-primary hover:bg-primary/20 mb-4">
                            <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
                            New: Human-in-the-Loop Engine v2.0
                        </div>
                        <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl md:text-7xl lg:text-8xl bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/70">
                            A hands-free inbox <br className="hidden md:block" />
                            powered by AI.
                        </h1>
                        <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl lg:text-2xl leading-relaxed">
                            Stop drowning in email. Our autonomous agents draft, triage, and reply for you—escalating only what matters to human experts.
                        </p>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-4 w-full justify-center pt-8">
                        <Link to="/signup">
                            <Button size="lg" className="rounded-full h-12 px-8 text-lg w-full sm:w-auto">
                                Start Free Trial <ArrowRight className="ml-2 h-5 w-5" />
                            </Button>
                        </Link>
                        <Button variant="outline" size="lg" className="rounded-full h-12 px-8 text-lg w-full sm:w-auto">
                            View Demo
                        </Button>
                    </div>

                    <div className="pt-12 text-sm text-muted-foreground flex items-center justify-center gap-8 opacity-70">
                        <div className="flex items-center gap-2">
                            <Shield className="h-4 w-4" /> SOC-2 Compliant
                        </div>
                        <div className="flex items-center gap-2">
                            <CheckCircle2 className="h-4 w-4" /> 99.9% Accuracy
                        </div>
                        <div className="flex items-center gap-2">
                            <Zap className="h-4 w-4" /> Instant Setup
                        </div>
                    </div>
                </section>

                {/* Social Proof */}
                <section className="border-y bg-muted/30 py-12">
                    <div className="container">
                        <p className="text-center text-sm font-semibold text-muted-foreground mb-8 uppercase tracking-widest">
                            Trusted by teams at forward-thinking companies
                        </p>
                        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
                            {/* Placeholders for logos */}
                            <div className="h-8 w-24 bg-foreground/20 rounded animate-pulse" />
                            <div className="h-8 w-24 bg-foreground/20 rounded animate-pulse" />
                            <div className="h-8 w-24 bg-foreground/20 rounded animate-pulse" />
                            <div className="h-8 w-24 bg-foreground/20 rounded animate-pulse" />
                            <div className="h-8 w-24 bg-foreground/20 rounded animate-pulse" />
                        </div>
                    </div>
                </section>

                {/* Features Grid */}
                <section id="features" className="container py-24 md:py-32 space-y-24">
                    <div className="grid md:grid-cols-2 gap-12 lg:gap-24 items-center">
                        <div className="space-y-6">
                            <div className="h-12 w-12 rounded-2xl bg-blue-500/10 flex items-center justify-center">
                                <Zap className="h-6 w-6 text-blue-500" />
                            </div>
                            <h2 className="text-3xl font-bold tracking-tight md:text-4xl">Autonomous Triage</h2>
                            <p className="text-lg text-muted-foreground">
                                Our Brain Organ scans every incoming message, categorizing them instantly. Spam is nuked, newsletters are summarized, and critical work is flagged.
                            </p>
                            <ul className="space-y-2">
                                {["Deep Context Understanding", "Zero-Latency Routing", "Custom Policy Engine"].map(item => (
                                    <li key={item} className="flex items-center gap-2 text-muted-foreground">
                                        <CheckCircle2 className="h-4 w-4 text-primary" /> {item}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="rounded-xl border bg-card p-2 shadow-2xl skew-y-1">
                            <div className="rounded-lg bg-muted/50 aspect-video flex items-center justify-center text-muted-foreground">
                                Feature UI Visualization
                            </div>
                        </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-12 lg:gap-24 items-center md:flex-row-reverse">
                        <div className="rounded-xl border bg-card p-2 shadow-2xl -skew-y-1 md:order-1">
                            <div className="rounded-lg bg-muted/50 aspect-video flex items-center justify-center text-muted-foreground">
                                HITL Dashboard Preview
                            </div>
                        </div>
                        <div className="space-y-6 md:order-2">
                            <div className="h-12 w-12 rounded-2xl bg-purple-500/10 flex items-center justify-center">
                                <Globe className="h-6 w-6 text-purple-500" />
                            </div>
                            <h2 className="text-3xl font-bold tracking-tight md:text-4xl">Human-in-the-Loop</h2>
                            <p className="text-lg text-muted-foreground">
                                When the AI is unsure, it doesn't guess. It escalates to our expert "Guide" agents who resolve ambiguity without you ever being bothered.
                            </p>
                            <ul className="space-y-2">
                                {["100% Accuracy Guarantee", "Seamless Escalation", "Continuous Learning Loop"].map(item => (
                                    <li key={item} className="flex items-center gap-2 text-muted-foreground">
                                        <CheckCircle2 className="h-4 w-4 text-primary" /> {item}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </section>
            </main>

            <footer className="border-t py-12 bg-muted/20">
                <div className="container grid md:grid-cols-4 gap-8">
                    <div className="space-y-4">
                        <div className="flex items-center gap-2 font-bold tracking-tighter">
                            <Mail className="h-5 w-5" />
                            <span>Assistants Co.</span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                            Building the operating system for the future of work.
                        </p>
                    </div>
                    <div>
                        <h3 className="font-semibold mb-4">Product</h3>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-foreground">Features</a></li>
                            <li><a href="#" className="hover:text-foreground">Pricing</a></li>
                            <li><a href="#" className="hover:text-foreground">Security</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="font-semibold mb-4">Company</h3>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-foreground">About</a></li>
                            <li><a href="#" className="hover:text-foreground">Blog</a></li>
                            <li><a href="#" className="hover:text-foreground">Careers</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="font-semibold mb-4">Legal</h3>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-foreground">Privacy</a></li>
                            <li><a href="#" className="hover:text-foreground">Terms</a></li>
                        </ul>
                    </div>
                </div>
                <div className="container mt-12 pt-8 border-t text-center text-xs text-muted-foreground">
                    © 2026 Assistants Company Incorp. All rights reserved.
                </div>
            </footer>
        </div>
    );
};

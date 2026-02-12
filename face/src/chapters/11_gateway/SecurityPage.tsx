
import React from 'react';
import { Button } from "@/components/ui/button";
import { Link } from 'react-router-dom';
import { Shield, Lock, FileText, CheckCircle2, Server, Eye, AlertTriangle } from "lucide-react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"

export const SecurityPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-background flex flex-col font-sans text-foreground selection:bg-primary/20">
            {/* Navigation (Simple) */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
                <div className="container flex h-16 items-center justify-between">
                    <Link to="/" className="font-bold text-xl tracking-tighter flex items-center gap-2">
                        <Shield className="h-5 w-5 text-primary" />
                        <span>Assistants Co. Security</span>
                    </Link>
                    <Link to="/">
                        <Button variant="ghost" size="sm">Back to Home</Button>
                    </Link>
                </div>
            </header>

            <main className="flex-1 container py-12 md:py-24 space-y-24">

                {/* Header */}
                <section className="text-center space-y-6 max-w-3xl mx-auto">
                    <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors border-transparent bg-green-500/10 text-green-500 mb-4">
                        <CheckCircle2 className="h-3 w-3 mr-1" />
                        System Operational
                    </div>
                    <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl">
                        Your data is yours. <br className="hidden md:block" />
                        We just protect it.
                    </h1>
                    <p className="text-xl text-muted-foreground">
                        We are built on a "Zero-Retention" architecture. We process your emails in volatile memory and discard them immediately after action.
                    </p>
                </section>

                {/* Core Pillars */}
                <section className="grid md:grid-cols-3 gap-8">
                    <div className="border rounded-xl p-8 space-y-4 bg-card/50">
                        <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                            <Lock className="h-5 w-5 text-primary" />
                        </div>
                        <h3 className="text-xl font-bold">Encryption at Rest & Transit</h3>
                        <p className="text-muted-foreground">
                            All data is encrypted via TLS 1.3 in transit and AES-256 at rest. Keys are managed via AWS KMS with strict rotation policies.
                        </p>
                    </div>
                    <div className="border rounded-xl p-8 space-y-4 bg-card/50">
                        <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                            <Eye className="h-5 w-5 text-primary" />
                        </div>
                        <h3 className="text-xl font-bold">No Human Access</h3>
                        <p className="text-muted-foreground">
                            Our engineers have zero access to your raw emails. HITL agents only see "anonymized snippets" strictly when you explicitly approve escalation.
                        </p>
                    </div>
                    <div className="border rounded-xl p-8 space-y-4 bg-card/50">
                        <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                            <Server className="h-5 w-5 text-primary" />
                        </div>
                        <h3 className="text-xl font-bold">Ephemeral Processing</h3>
                        <p className="text-muted-foreground">
                            Our "Spine" architecture ensures emails are processed in stateless workers. Once the LLM generates a draft, the source content is wiped.
                        </p>
                    </div>
                </section>

                {/* FAQ */}
                <section className="max-w-3xl mx-auto w-full space-y-8">
                    <h2 className="text-3xl font-bold text-center">Frequently Asked Questions</h2>
                    <Accordion type="single" collapsible className="w-full">
                        <AccordionItem value="item-1">
                            <AccordionTrigger>Do you train your AI on my emails?</AccordionTrigger>
                            <AccordionContent>
                                <strong>No.</strong> We use pre-trained foundational models. We do not use your personal data to train our global models. Any fine-tuning (if enabled) is strictly local to your tenant and isolated.
                            </AccordionContent>
                        </AccordionItem>
                        <AccordionItem value="item-2">
                            <AccordionTrigger>What happens if I delete my account?</AccordionTrigger>
                            <AccordionContent>
                                We execute a "Hard Delete". All your metadata, logs, and tenant configurations are meticulously wiped from our databases within 24 hours.
                            </AccordionContent>
                        </AccordionItem>
                        <AccordionItem value="item-3">
                            <AccordionTrigger>Are you SOC-2 Compliant?</AccordionTrigger>
                            <AccordionContent>
                                We are currently in the <strong>Type I</strong> audit phase. We expect full certification by Q3 2026. Our infrastructure is already mapped to SOC-2 controls.
                            </AccordionContent>
                        </AccordionItem>
                        <AccordionItem value="item-4">
                            <AccordionTrigger>How do you handle Google OAuth scopes?</AccordionTrigger>
                            <AccordionContent>
                                We request the minimum viable scope: <code>gmail.modify</code>. This allows us to read emails to triage them and create drafts. We never send emails without your approval unless you enable "Fully Autonomous" mode.
                            </AccordionContent>
                        </AccordionItem>
                    </Accordion>
                </section>

                {/* Compliance Badges (Grayscale) */}
                <section className="border-t py-12">
                    <div className="flex justify-center gap-12 opacity-40 grayscale">
                        <div className="flex flex-col items-center gap-2">
                            <Shield className="h-12 w-12" />
                            <span className="font-bold text-xs">SOC 2 Type I</span>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                            <FileText className="h-12 w-12" />
                            <span className="font-bold text-xs">GDPR Ready</span>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                            <Lock className="h-12 w-12" />
                            <span className="font-bold text-xs">HIPAA Capable</span>
                        </div>
                    </div>
                </section>

                {/* Report Issue */}
                <section className="bg-muted/30 rounded-2xl p-8 md:p-12 text-center space-y-6">
                    <AlertTriangle className="h-12 w-12 mx-auto text-yellow-500" />
                    <h2 className="text-2xl font-bold">Found a vulnerability?</h2>
                    <p className="text-muted-foreground max-w-xl mx-auto">
                        We value security researchers. If you believe you've found a security issue, please report it to our security team immediately.
                    </p>
                    <a href="mailto:security@assistants.co">
                        <Button variant="outline">Contact Security Team</Button>
                    </a>
                </section>

            </main>

            <footer className="border-t py-8 text-center text-xs text-muted-foreground">
                <div className="container">
                    <p>© 2026 Assistants Company Incorp. Security Center.</p>
                </div>
            </footer>
        </div>
    );
};

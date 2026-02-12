
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { admin } from "@/lib/api";
import { Loader2, DollarSign, FileText } from "lucide-react";
import { ReconciliationReport } from './ReconciliationReport';

interface BillingPanelProps {
    tenantId: string | null;
}

interface LedgerData {
    balance: number;
    currency: string;
    history: {
        id: number;
        timestamp: string;
        amount: number;
        description: string;
        stripe_charge_id?: string;
    }[];
}

export const BillingPanel: React.FC<BillingPanelProps> = ({ tenantId }) => {
    const [data, setData] = useState<LedgerData | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!tenantId) return;

        const fetchLedger = async () => {
            setLoading(true);
            try {
                const res = await admin.getLedger(tenantId);
                setData(res);
            } catch (err) {
                console.error("Failed to fetch ledger", err);
            } finally {
                setLoading(false);
            }
        };
        fetchLedger();
    }, [tenantId]);

    if (!tenantId) {
        return (
            <div className="flex flex-col items-center justify-center p-12 text-muted-foreground">
                <FileText className="h-12 w-12 mb-4 opacity-20" />
                <p>Select a tenant to view billing details.</p>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="flex justify-center p-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    if (!data) return null;

    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount / 100);
    };

    return (
        <div className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Current Balance</CardTitle>
                        <DollarSign className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{formatCurrency(data.balance)}</div>
                        <p className="text-xs text-muted-foreground">
                            {data.balance < 0 ? "Credit Remaining" : "Amount Due"}
                        </p>
                    </CardContent>
                </Card>
            </div>

            <ReconciliationReport ledgerData={data} />

            <Card>
                <CardHeader>
                    <CardTitle>Transaction Ledger</CardTitle>
                    <CardDescription>Immutable record of all financial activity for this tenant.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Date</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead>Stripe ID</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {data.history.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={4} className="text-center h-24 text-muted-foreground">
                                        No transactions found.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                data.history.map((tx) => (
                                    <TableRow key={tx.id}>
                                        <TableCell>{new Date(tx.timestamp).toLocaleDateString()}</TableCell>
                                        <TableCell>{tx.description}</TableCell>
                                        <TableCell>
                                            {tx.stripe_charge_id ? (
                                                <Badge variant="outline" className="font-mono text-xs">
                                                    {tx.stripe_charge_id}
                                                </Badge>
                                            ) : (
                                                <span className="text-muted-foreground text-xs">-</span>
                                            )}
                                        </TableCell>
                                        <TableCell className={`text-right font-medium ${tx.amount > 0 ? 'text-destructive' : 'text-green-600'}`}>
                                            {formatCurrency(tx.amount)}
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
};

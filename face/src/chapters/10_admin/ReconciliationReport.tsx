
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle, CheckCircle2 } from "lucide-react";

interface ReconciliationReportProps {
    ledgerData: {
        balance: number;
        history: any[];
    };
}

export const ReconciliationReport: React.FC<ReconciliationReportProps> = ({ ledgerData }) => {
    // Basic check: Sum of history should equal balance (Client-side verification of server math)
    const calculatedBalance = ledgerData.history.reduce((acc, curr) => acc + curr.amount, 0);
    const isBalanced = Math.abs(calculatedBalance - ledgerData.balance) < 0.01;

    return (
        <Card className={isBalanced ? "border-green-200 bg-green-50/10" : "border-destructive/50 bg-destructive/5"}>
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    Start-of-Day Reconciliation
                    {isBalanced ? (
                        <span className="text-green-600 flex items-center text-xs ml-auto">
                            <CheckCircle2 className="w-3 h-3 mr-1" />
                            Balanced
                        </span>
                    ) : (
                        <span className="text-destructive flex items-center text-xs ml-auto">
                            <AlertCircle className="w-3 h-3 mr-1" />
                            Drift Detected
                        </span>
                    )}
                </CardTitle>
            </CardHeader>
            <CardContent>
                {isBalanced ? (
                    <p className="text-xs text-muted-foreground">
                        Internal Ledger matches calculated transaction history. No anomalies detected in Stripe synchronization.
                    </p>
                ) : (
                    <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>Ledger Mismatch</AlertTitle>
                        <AlertDescription>
                            Calculated sum ({calculatedBalance}) does not match stored balance ({ledgerData.balance}).
                            Immediate investigation required.
                        </AlertDescription>
                    </Alert>
                )}
            </CardContent>
        </Card>
    );
};

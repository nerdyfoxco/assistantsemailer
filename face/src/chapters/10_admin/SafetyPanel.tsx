
import { useState, useEffect } from 'react';
import { admin } from '../../lib/api';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '../../components/ui/alert';
import { AlertTriangle, Power, ShieldCheck } from 'lucide-react';

export function SafetyPanel() {
    const [status, setStatus] = useState<"OPERATIONAL" | "HALTED">("OPERATIONAL");
    const [lastUpdated, setLastUpdated] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const refreshStatus = async () => {
        try {
            const data = await admin.getSafetyStatus();
            setStatus(data.status);
            setLastUpdated(data.last_updated);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        refreshStatus();
        const interval = setInterval(refreshStatus, 5000); // Poll every 5s
        return () => clearInterval(interval);
    }, []);

    const toggleSwitch = async () => {
        const action = status === "OPERATIONAL" ? "KILL" : "RESUME";
        if (!confirm(`Are you sure you want to ${action} the system? This implies GLOBAL impact.`)) return;

        setLoading(true);
        try {
            if (status === "OPERATIONAL") {
                await admin.engageKillSwitch();
            } else {
                await admin.disengageKillSwitch();
            }
            await refreshStatus();
        } catch (e) {
            alert("Failed to toggle safety switch");
        } finally {
            setLoading(false);
        }
    };

    const isHalted = status === "HALTED";

    return (
        <Card className={`border-l-4 ${isHalted ? 'border-l-red-500 bg-red-50' : 'border-l-green-500'}`}>
            <CardHeader>
                <div className="flex justify-between items-center">
                    <div>
                        <CardTitle className="flex items-center gap-2">
                            {isHalted ? <AlertTriangle className="text-red-500" /> : <ShieldCheck className="text-green-500" />}
                            System Safety
                        </CardTitle>
                        <CardDescription>Global controls for emergency stopping.</CardDescription>
                    </div>
                    {isHalted && (
                        <div className="text-red-600 font-bold animate-pulse text-lg">
                            SYSTEM HALTED
                        </div>
                    )}
                </div>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col gap-4">
                    <Alert variant={isHalted ? "destructive" : "default"}>
                        <AlertTitle>Current Status: {status}</AlertTitle>
                        <AlertDescription>
                            {lastUpdated ? `Last updated: ${new Date(lastUpdated).toLocaleString()}` : "No status change logged."}
                        </AlertDescription>
                    </Alert>

                    <Button
                        variant={isHalted ? "default" : "destructive"}
                        size="lg"
                        className="w-full h-16 text-xl font-bold"
                        onClick={toggleSwitch}
                        disabled={loading}
                    >
                        <Power className="mr-2 h-6 w-6" />
                        {loading ? "Processing..." : (isHalted ? "RESUME OPERATIONS" : "EMERGENCY STOP (KILL SWITCH)")}
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}

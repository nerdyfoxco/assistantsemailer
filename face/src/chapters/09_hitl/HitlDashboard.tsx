import { useState, useEffect } from 'react';
import { hitl } from '../../lib/api';
import type { HitlRequest } from '../../lib/api';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Loader2, AlertCircle } from 'lucide-react';
import { ResolutionCard } from './ResolutionCard';

export function HitlDashboard() {
    const [queue, setQueue] = useState<HitlRequest[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedReq, setSelectedReq] = useState<HitlRequest | null>(null);
    const [agentId] = useState("agent-007"); // Hardcoded for v0

    const refreshQueue = async () => {
        setLoading(true);
        try {
            const data = await hitl.getQueue("t1"); // Hardcoded Tenant for v0
            setQueue(data);
        } catch (e) {
            console.error("Failed to fetch queue", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        refreshQueue();
    }, []);

    const handleClaim = async (req: HitlRequest) => {
        try {
            await hitl.claimRequest(req.id, agentId);
            // Optimistic update
            setSelectedReq({ ...req, state: "CLAIMED", claimed_by_agent_id: agentId });
            refreshQueue(); // Refresh to remove from pending view or update status
        } catch (e) {
            alert("Failed to claim request");
        }
    };

    const handleResolutionComplete = () => {
        setSelectedReq(null);
        refreshQueue();
    };

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold tracking-tight">Escalation Queue</h1>
                <Button variant="outline" onClick={refreshQueue} disabled={loading}>
                    {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : "Refresh"}
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left: The Queue List */}
                <div className="md:col-span-1 space-y-4">
                    {queue.length === 0 && !loading && (
                        <Card>
                            <CardContent className="pt-6 text-center text-muted-foreground">
                                No pending items. Good job!
                            </CardContent>
                        </Card>
                    )}

                    {queue.map(req => (
                        <Card
                            key={req.id}
                            className={`cursor-pointer hover:bg-accent transition-colors ${selectedReq?.id === req.id ? 'border-primary ring-1 ring-primary' : ''}`}
                            onClick={() => handleClaim(req)}
                        >
                            <CardHeader className="p-4">
                                <div className="flex justify-between items-start">
                                    <CardTitle className="text-sm font-medium">
                                        {req.reason}
                                    </CardTitle>
                                    <Badge variant={req.state === "CLAIMED" ? "default" : "secondary"}>
                                        {req.state}
                                    </Badge>
                                </div>
                                <div className="text-xs text-muted-foreground mt-2">
                                    ID: {req.id.slice(0, 8)}...
                                </div>
                                <div className="text-xs text-muted-foreground">
                                    {new Date(req.created_at).toLocaleTimeString()}
                                </div>
                            </CardHeader>
                        </Card>
                    ))}
                </div>

                {/* Right: The Workspace */}
                <div className="md:col-span-2">
                    {selectedReq ? (
                        <ResolutionCard
                            request={selectedReq}
                            agentId={agentId}
                            onComplete={handleResolutionComplete}
                        />
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-muted-foreground border-2 border-dashed rounded-lg p-12">
                            <AlertCircle className="h-12 w-12 mb-4 opacity-50" />
                            <p>Select an item to claim and resolve.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

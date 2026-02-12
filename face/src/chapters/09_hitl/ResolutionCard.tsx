import { useState } from 'react';
import { hitl } from '../../lib/api';
import type { HitlRequest, HitlDecision } from '../../lib/api';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Textarea } from '../../components/ui/textarea';
import { Label } from '../../components/ui/label';
import { Badge } from '../../components/ui/badge';
import { CheckCircle, XCircle, PenTool } from 'lucide-react';

interface ResolutionCardProps {
    request: HitlRequest;
    agentId: string;
    onComplete: () => void;
}

export function ResolutionCard({ request, agentId, onComplete }: ResolutionCardProps) {
    const context = JSON.parse((request as any).context_json || "{}");
    const [draft, setDraft] = useState(context.draft_body || "");
    const [notes, setNotes] = useState("");
    const [isEditing, setIsEditing] = useState(false);
    const [submitting, setSubmitting] = useState(false);

    const handleResolve = async (outcome: "RESOLVED" | "REJECTED") => {
        setSubmitting(true);
        try {
            const decision: HitlDecision = {
                request_id: request.id,
                agent_id: agentId,
                outcome: outcome,
                modified_draft: isEditing || draft !== context.draft_body ? draft : undefined,
                feedback_notes: notes
            };
            await hitl.resolveRequest(decision);
            onComplete();
        } catch (e) {
            alert("Failed to submit resolution");
        } finally {
            setSubmitting(false);
        }
    };

    if (request.state !== "CLAIMED") {
        return (
            <Card>
                <CardContent className="pt-6 text-center">
                    Please claim this request to start working.
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="border-b bg-muted/20">
                <div className="flex justify-between items-center">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <PenTool className="h-5 w-5" />
                        Resolution Workspace
                    </CardTitle>
                    <Badge variant="outline" className="font-mono">
                        {request.id}
                    </Badge>
                </div>
            </CardHeader>

            <CardContent className="flex-1 overflow-y-auto p-6 space-y-6">
                <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <Label className="text-muted-foreground">Reason</Label>
                            <p className="font-medium">{request.reason}</p>
                        </div>
                        <div>
                            <Label className="text-muted-foreground">Original Sender</Label>
                            <p className="font-medium">{context.from_email || "Unknown"}</p>
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label>Context / Original Email</Label>
                        <div className="bg-muted p-4 rounded-md text-sm whitespace-pre-wrap max-h-48 overflow-y-auto">
                            {context.email_body || "No email body content available."}
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between items-center">
                            <Label>Proposed Draft</Label>
                            <Button variant="ghost" size="sm" onClick={() => setIsEditing(!isEditing)}>
                                {isEditing ? "Cancel Edit" : "Edit Draft"}
                            </Button>
                        </div>
                        {isEditing ? (
                            <Textarea
                                value={draft}
                                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setDraft(e.target.value)}
                                className="min-h-[200px] font-mono text-sm"
                            />
                        ) : (
                            <div className="border rounded-md p-4 min-h-[100px] text-sm whitespace-pre-wrap bg-card">
                                {draft || <span className="text-muted-foreground italic">No draft proposed.</span>}
                            </div>
                        )}
                    </div>

                    <div className="space-y-2">
                        <Label>Feedback Notes (Optional)</Label>
                        <Textarea
                            placeholder="Why did you change this? (Helps training)"
                            value={notes}
                            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setNotes(e.target.value)}
                        />
                    </div>
                </div>
            </CardContent>

            <CardFooter className="border-t bg-muted/20 p-4 flex justify-between">
                <Button
                    variant="destructive"
                    onClick={() => handleResolve("REJECTED")}
                    disabled={submitting}
                >
                    <XCircle className="mr-2 h-4 w-4" />
                    Reject (Do Not Send)
                </Button>
                <div className="space-x-2">
                    <Button
                        variant="default"
                        className="bg-green-600 hover:bg-green-700"
                        onClick={() => handleResolve("RESOLVED")}
                        disabled={submitting}
                    >
                        <CheckCircle className="mr-2 h-4 w-4" />
                        {isEditing ? "Approve Changes" : "Approve Draft"}
                    </Button>
                </div>
            </CardFooter>
        </Card>
    );
}


import React from 'react';
import { useMind } from './MindContext';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Brain, Check, X, Loader2 } from 'lucide-react';
import { Badge } from '../../components/ui/badge';

interface DecisionCardProps {
    messageId: string;
}

export const DecisionCard: React.FC<DecisionCardProps> = ({ messageId }) => {
    const { decision, isThinking, error, analyzeEmail, executeDecision, clearDecision } = useMind();

    if (error) {
        return (
            <div className="p-4 bg-red-50 text-red-600 rounded-md flex items-center gap-2">
                <X className="w-4 h-4" />
                <span>Error: {error}</span>
                <Button variant="ghost" size="sm" onClick={() => analyzeEmail(messageId)}>Retry</Button>
            </div>
        );
    }

    if (isThinking) {
        return (
            <Card className="w-full animate-pulse border-purple-200 bg-purple-50">
                <CardContent className="p-6 flex items-center justify-center gap-3">
                    <Loader2 className="w-6 h-6 animate-spin text-purple-600" />
                    <span className="text-purple-700 font-medium">Strategist is thinking...</span>
                </CardContent>
            </Card>
        );
    }

    if (!decision) {
        return (
            <div className="flex justify-center p-4">
                <Button
                    variant="outline"
                    className="gap-2 text-purple-700 border-purple-200 hover:bg-purple-50"
                    onClick={() => analyzeEmail(messageId)}
                >
                    <Brain className="w-4 h-4" />
                    Ask Strategist
                </Button>
            </div>
        );
    }

    return (
        <Card className="w-full border-purple-200 shadow-sm overflow-hidden">
            <CardHeader className="bg-purple-50/50 pb-3">
                <div className="flex justify-between items-center">
                    <CardTitle className="text-sm font-medium text-purple-900 flex items-center gap-2">
                        <Brain className="w-4 h-4 text-purple-600" />
                        Proposed Action: <span className="font-bold">{decision.action}</span>
                    </CardTitle>
                    <div className="flex gap-1">
                        {decision.tags.map(tag => (
                            <Badge key={tag} variant="secondary" className="text-xs bg-purple-100 text-purple-700">
                                {tag}
                            </Badge>
                        ))}
                    </div>
                </div>
            </CardHeader>
            <CardContent className="p-4 space-y-3">
                <div className="text-sm text-gray-600 italic border-l-2 border-purple-200 pl-3">
                    "{decision.reasoning}"
                </div>

                {decision.draft_body && (
                    <div className="bg-white p-3 rounded-md border border-gray-200 text-sm font-mono text-gray-700 whitespace-pre-wrap">
                        {decision.draft_body}
                    </div>
                )}
            </CardContent>
            <CardFooter className="bg-gray-50 p-3 flex justify-end gap-2">
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={clearDecision}
                    className="text-gray-500 hover:text-gray-700"
                >
                    Dismiss
                </Button>
                <Button
                    size="sm"
                    className="bg-purple-600 hover:bg-purple-700 text-white gap-2"
                    onClick={() => executeDecision(messageId, decision)}
                >
                    <Check className="w-4 h-4" />
                    Approve & Execute
                </Button>
            </CardFooter>
        </Card>
    );
};

import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Copy, Plus, Trash2, Key, AlertTriangle, Check, Loader2 } from "lucide-react";
import { api } from '@/lib/api';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogFooter
} from "@/components/ui/dialog";

interface ApiKey {
    id: string;
    name: string;
    prefix: string;
    created_at: string;
    scopes: string[];
}

export const KeyManager: React.FC = () => {
    const [keys, setKeys] = useState<ApiKey[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isGenerating, setIsGenerating] = useState(false);

    // New Key State
    const [newKeyName, setNewKeyName] = useState("");
    const [rawKey, setRawKey] = useState<string | null>(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);

    useEffect(() => {
        fetchKeys();
    }, []);

    const fetchKeys = async () => {
        try {
            const res = await api.get<ApiKey[]>('/developer/keys');
            setKeys(res.data);
        } catch (err) {
            console.error("Failed to fetch keys", err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenerateKey = async () => {
        setIsGenerating(true);
        try {
            const res = await api.post('/developer/keys', { name: newKeyName });
            setRawKey(res.data.raw_key);
            fetchKeys(); // Refresh list
        } catch (err) {
            console.error("Failed to generate key", err);
        } finally {
            setIsGenerating(false);
        }
    };

    const handleRevokeKey = async (id: string) => {
        if (!confirm("Are you sure? This action cannot be undone and will break any integrations using this key.")) return;

        try {
            await api.delete(`/developer/keys/${id}`);
            fetchKeys();
        } catch (err) {
            console.error("Failed to revoke key", err);
        }
    };

    const copyToClipboard = () => {
        if (rawKey) {
            navigator.clipboard.writeText(rawKey);
            alert("Copied to clipboard!");
        }
    };

    const closeDialog = () => {
        setIsDialogOpen(false);
        setRawKey(null);
        setNewKeyName("");
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight">API Keys</h2>
                    <p className="text-muted-foreground">Manage API keys for accessing the Assistant Emailer Platform.</p>
                </div>
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                    <DialogTrigger asChild>
                        <Button>
                            <Plus className="mr-2 h-4 w-4" /> Generate New Key
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Generate API Key</DialogTitle>
                            <DialogDescription>
                                Create a new key to access the API programmatically.
                            </DialogDescription>
                        </DialogHeader>

                        {!rawKey ? (
                            <div className="space-y-4 py-4">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Key Name</label>
                                    <Input
                                        placeholder="e.g. CI/CD Pipeline"
                                        value={newKeyName}
                                        onChange={(e) => setNewKeyName(e.target.value)}
                                    />
                                </div>
                            </div>
                        ) : (
                            <div className="space-y-4 py-4">
                                <div className="rounded-md bg-yellow-50 p-4 border border-yellow-200">
                                    <div className="flex">
                                        <div className="flex-shrink-0">
                                            <AlertTriangle className="h-5 w-5 text-yellow-400" aria-hidden="true" />
                                        </div>
                                        <div className="ml-3">
                                            <h3 className="text-sm font-medium text-yellow-800">Save this key now</h3>
                                            <div className="mt-2 text-sm text-yellow-700">
                                                <p>This is the only time we will show you the full API key. Make sure to copy it now.</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="flex-1 p-3 bg-muted rounded-md font-mono text-sm break-all">
                                        {rawKey}
                                    </div>
                                    <Button variant="outline" size="icon" onClick={copyToClipboard}>
                                        <Copy className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        )}

                        <DialogFooter>
                            {!rawKey ? (
                                <Button onClick={handleGenerateKey} disabled={!newKeyName || isGenerating}>
                                    {isGenerating && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                    Generate Key
                                </Button>
                            ) : (
                                <Button onClick={closeDialog}>Done</Button>
                            )}
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            <div className="border rounded-lg">
                <table className="w-full text-sm">
                    <thead>
                        <tr className="border-b bg-muted/50">
                            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground w-[40%]">Name</th>
                            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Prefix</th>
                            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Created</th>
                            <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? (
                            <tr>
                                <td colSpan={4} className="p-4 text-center text-muted-foreground">Loading keys...</td>
                            </tr>
                        ) : keys.length === 0 ? (
                            <tr>
                                <td colSpan={4} className="p-8 text-center text-muted-foreground">
                                    <Key className="mx-auto h-8 w-8 mb-3 opacity-20" />
                                    No API keys found. Generate one to get started.
                                </td>
                            </tr>
                        ) : (
                            keys.map((key) => (
                                <tr key={key.id} className="border-b last:border-0 hover:bg-muted/50 transition-colors">
                                    <td className="p-4 font-medium">{key.name}</td>
                                    <td className="p-4 font-mono text-xs text-muted-foreground">{key.prefix}...</td>
                                    <td className="p-4 text-muted-foreground">{new Date(key.created_at).toLocaleDateString()}</td>
                                    <td className="p-4 text-right">
                                        <Button variant="ghost" size="icon" className="text-red-500 hover:text-red-600 hover:bg-red-50" onClick={() => handleRevokeKey(key.id)}>
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

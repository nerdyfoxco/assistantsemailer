import { useEffect, useState } from 'react';
import { api } from '../../lib/api';
import { Loader2, RefreshCw } from 'lucide-react';
import { cn } from '../../lib/utils'; // Assuming utils exists

interface WorkItem {
    id: string;
    email_id: string;
    state: string;
    priority: number;
    created_at: string;
}

export function WorkItemList() {
    const [items, setItems] = useState<WorkItem[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchItems = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.get('/work-items/');
            setItems(response.data);
        } catch (err) {
            console.error(err);
            setError("Failed to load work items.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchItems();
    }, []);

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold tracking-tight">Work Items</h2>
                <button
                    onClick={fetchItems}
                    disabled={isLoading}
                    className="inline-flex items-center px-3 py-1.5 text-sm font-medium border rounded-md hover:bg-neutral-100 disabled:opacity-50"
                >
                    <RefreshCw className={cn("h-4 w-4 mr-2", isLoading && "animate-spin")} />
                    Refresh
                </button>
            </div>

            {error && (
                <div className="p-4 bg-red-50 text-red-600 rounded-md border border-red-200">
                    {error}
                </div>
            )}

            <div className="border rounded-md bg-card overflow-hidden shadow-sm">
                <table className="w-full text-sm text-left">
                    <thead className="bg-neutral-50 border-b text-muted-foreground uppercase text-xs">
                        <tr>
                            <th className="px-6 py-3 font-medium">ID</th>
                            <th className="px-6 py-3 font-medium">State</th>
                            <th className="px-6 py-3 font-medium">Priority</th>
                            <th className="px-6 py-3 font-medium">Created</th>
                            <th className="px-6 py-3 font-medium text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y">
                        {isLoading && items.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="px-6 py-12 text-center text-muted-foreground">
                                    <Loader2 className="h-6 w-6 animate-spin mx-auto mb-2" />
                                    Loading...
                                </td>
                            </tr>
                        ) : items.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="px-6 py-12 text-center text-muted-foreground">
                                    No work items found.
                                </td>
                            </tr>
                        ) : (
                            items.map((item) => (
                                <tr key={item.id} className="hover:bg-neutral-50/50">
                                    <td className="px-6 py-4 font-mono text-xs">{item.id.substring(0, 8)}...</td>
                                    <td className="px-6 py-4">
                                        <span className={cn(
                                            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                                            item.state === 'NEEDS_REPLY' ? "bg-amber-100 text-amber-800" :
                                                item.state === 'DONE' ? "bg-green-100 text-green-800" :
                                                    "bg-neutral-100 text-neutral-800"
                                        )}>
                                            {item.state}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">{item.priority}</td>
                                    <td className="px-6 py-4 text-muted-foreground">
                                        {new Date(item.created_at).toLocaleDateString()}
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <button className="text-primary hover:underline">
                                            View
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

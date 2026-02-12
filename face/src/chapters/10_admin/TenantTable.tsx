
import { useState } from 'react';
import { admin } from '../../lib/api';
import type { Tenant } from '../../lib/types';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Badge } from '../../components/ui/badge';

interface TenantTableProps {
    tenants: Tenant[];
    onRefresh: () => void;
    onSelect?: (tenant: Tenant) => void;
}

export function TenantTable({ tenants, onRefresh, onSelect }: TenantTableProps) {
    const [loading, setLoading] = useState<string | null>(null);

    const handleSuspend = async (tenantId: string) => {
        if (!confirm("Are you sure you want to suspend this tenant?")) return;
        setLoading(tenantId);
        try {
            await admin.suspendTenant(tenantId);
            onRefresh();
        } catch (e) {
            alert("Failed to suspend tenant");
        } finally {
            setLoading(null);
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Tenants ({tenants.length})</CardTitle>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Name</TableHead>
                            <TableHead>Tier</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Created</TableHead>
                            <TableHead>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {tenants.map((t) => (
                            <TableRow key={t.id}>
                                <TableCell className="font-medium">{t.name}</TableCell>
                                <TableCell><Badge variant="outline">{t.tier}</Badge></TableCell>
                                <TableCell>
                                    <Badge variant={t.status === 'ACTIVE' ? 'default' : 'destructive'}>
                                        {t.status}
                                    </Badge>
                                </TableCell>
                                <TableCell>{new Date(t.created_at).toLocaleDateString()}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="secondary"
                                        size="sm"
                                        onClick={() => onSelect?.(t)}
                                        className="mr-2"
                                    >
                                        Select
                                    </Button>
                                    <Button
                                        variant="destructive"
                                        size="sm"
                                        disabled={loading === t.id || t.status === 'SUSPENDED'}
                                        onClick={() => handleSuspend(t.id)}
                                    >
                                        {loading === t.id ? "..." : "Suspend"}
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
    );
}

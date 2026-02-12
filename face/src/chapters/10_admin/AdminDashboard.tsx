
import { useState } from 'react';
import { admin } from '../../lib/api';
import type { Organization, Tenant } from '../../lib/api';
import { TenantTable } from './TenantTable';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { SafetyPanel } from './SafetyPanel';
import { BillingPanel } from './BillingPanel';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';

export function AdminDashboard() {
    const [orgId, setOrgId] = useState("");
    const [org, setOrg] = useState<Organization | null>(null);
    const [tenants, setTenants] = useState<Tenant[]>([]);
    const [selectedTenant, setSelectedTenant] = useState<Tenant | null>(null);
    const [newTenantName, setNewTenantName] = useState("");
    const [loading, setLoading] = useState(false);

    const loadHierarchy = async (oid: string) => {
        setLoading(true);
        try {
            const data = await admin.getHierarchy(oid);
            setOrg(data.organization);
            setTenants(data.tenants);
        } catch (e) {
            console.error(e);
            alert("Failed to load organization");
        } finally {
            setLoading(false);
        }
    };

    const handleCreateTenant = async () => {
        if (!org || !newTenantName) return;
        try {
            await admin.createTenant(org.id, newTenantName, "SOLO");
            setNewTenantName("");
            loadHierarchy(org.id);
        } catch (e) {
            alert("Failed to create tenant");
        }
    };

    return (
        <div className="p-6 space-y-6">
            <h1 className="text-3xl font-bold tracking-tight">The Overseer</h1>

            <div className="flex gap-4 items-end">
                <div className="grid w-full max-w-sm items-center gap-1.5">
                    <label htmlFor="orgId" className="text-sm font-medium">Organization ID</label>
                    <Input
                        id="orgId"
                        placeholder="UUID..."
                        value={orgId}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setOrgId(e.target.value)}
                    />
                </div>
                <Button onClick={() => loadHierarchy(orgId)} disabled={loading}>
                    {loading ? "Loading..." : "Load Hierarchy"}
                </Button>
            </div>

            {org && (
                <Tabs defaultValue="tenants" className="space-y-4">
                    <TabsList>
                        <TabsTrigger value="tenants">Tenants</TabsTrigger>
                        <TabsTrigger value="billing">Billing</TabsTrigger>
                        <TabsTrigger value="safety">System Safety</TabsTrigger>
                    </TabsList>

                    <TabsContent value="tenants" className="space-y-4">
                        <Card>
                            <CardHeader>
                                <CardTitle>Organization: {org.name}</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="flex gap-2">
                                    <Input
                                        placeholder="New Tenant Name"
                                        value={newTenantName}
                                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewTenantName(e.target.value)}
                                    />
                                    <Button onClick={handleCreateTenant}>Create Tenant</Button>
                                </div>
                            </CardContent>
                        </Card>
                        <TenantTable
                            tenants={tenants}
                            onRefresh={() => loadHierarchy(org.id)}
                            onSelect={setSelectedTenant}
                        />
                    </TabsContent>

                    <TabsContent value="billing" className="space-y-4">
                        <Card>
                            <CardHeader>
                                <CardTitle>Billing & Reconciliation</CardTitle>
                                <div className="text-sm text-muted-foreground">
                                    {selectedTenant
                                        ? `Viewing Ledger for: ${selectedTenant.name} (${selectedTenant.id})`
                                        : "Select a tenant from the Tenants tab to view billing details."}
                                </div>
                            </CardHeader>
                            <CardContent>
                                <BillingPanel tenantId={selectedTenant?.id || null} />
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="safety" className="space-y-4">
                        <SafetyPanel />
                    </TabsContent>
                </Tabs>
            )}
        </div>
    );
}

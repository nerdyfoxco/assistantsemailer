import { DashboardLayout } from '../components/layout/DashboardLayout';
import { WorkItemList } from '../features/dashboard/WorkItemList';

export function DashboardPage() {
    return (
        <DashboardLayout>
            <div className="space-y-6">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-slate-900">Dashboard</h1>
                    <p className="text-muted-foreground">Manage your email workflows and tasks.</p>
                </div>

                <WorkItemList />
            </div>
        </DashboardLayout>
    );
}

import { DashboardLayout } from '../components/layout/DashboardLayout';
import { WorkItemList } from '../features/dashboard/WorkItemList';
import { ConnectGmailButton } from '../features/auth/ConnectGmailButton';
import { EmailList } from '../features/dashboard/EmailList';

export function DashboardPage() {
    return (
        <DashboardLayout>
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Dashboard</h1>
                        <p className="text-muted-foreground">Manage your email workflows and tasks.</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <ConnectGmailButton />
                    </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                    <div className="col-span-4 space-y-4">
                        <EmailList />
                        <WorkItemList />
                    </div>

                    <div className="col-span-3 space-y-4">
                        <div className="rounded-xl border bg-card text-card-foreground shadow">
                            <div className="p-6">
                                <h3 className="font-semibold leading-none tracking-tight">Quick Stats</h3>
                                <p className="text-sm text-muted-foreground mt-2">Coming soon...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}

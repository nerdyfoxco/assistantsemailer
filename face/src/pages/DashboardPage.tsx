import { DashboardLayout } from '../components/layout/DashboardLayout';
import { WorkItemList } from '../features/dashboard/WorkItemList';
import { ConnectGmailButton } from '../features/auth/ConnectGmailButton';
import { useState, useEffect } from 'react'; // Assuming useState and useEffect are used
import { api } from '../lib/api'; // Assuming api is used

export function DashboardPage() {
    const [workItems, setWorkItems] = useState([]); // Assuming state for work items

    useEffect(() => {
        api.get('/work-items/').then(res => setWorkItems(res.data));
    }, []);

    return (
        <DashboardLayout>
            <div className="space-y-6">
                <div className="flex items-center justify-between"> {/* Adjusted div for layout */}
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Dashboard</h1>
                        <p className="text-muted-foreground">Manage your email workflows and tasks.</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <ConnectGmailButton />
                        <button
                            onClick={() => {
                                api.get('/work-items/').then(res => setWorkItems(res.data));
                            }}
                            className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2" // Added some basic styling for the button
                        >
                            Refresh Work Items
                        </button>
                    </div>
                </div>

                <WorkItemList workItems={workItems} /> {/* Pass workItems to WorkItemList */}
            </div>
        </DashboardLayout>
    );
}

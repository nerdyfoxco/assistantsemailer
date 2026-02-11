
import { cn } from '../../lib/utils';
import { LayoutDashboard, Inbox, User, LogOut } from 'lucide-react';
import { Link, useLocation, Outlet } from 'react-router-dom';

// interface DashboardLayoutProps {
//     children?: ReactNode;
// }

export function DashboardLayout() {
    const location = useLocation();

    const navItems = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Work Items', href: '/work-items', icon: Inbox },
        { name: 'Intelligence', href: '/intelligence', icon: Inbox }, // Added Intelligence Link
        { name: 'Profile', href: '/profile', icon: User },
    ];

    return (
        <div className="min-h-screen bg-neutral-100 flex">
            {/* Sidebar */}
            <aside className="w-64 bg-card border-r hidden md:flex flex-col">
                <div className="p-6 border-b">
                    <h1 className="text-xl font-bold text-primary">Spine + Face</h1>
                </div>
                <nav className="flex-1 p-4 space-y-2">
                    {navItems.map((item) => (
                        <Link
                            key={item.name}
                            to={item.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer",
                                location.pathname === item.href ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-neutral-100 hover:text-foreground"
                            )}
                        >
                            <item.icon className="h-4 w-4" />
                            {item.name}
                        </Link>
                    ))}
                </nav>
                <div className="p-4 border-t">
                    <button className="flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium text-destructive hover:bg-destructive/10 w-full transition-colors">
                        <LogOut className="h-4 w-4" />
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-8 overflow-y-auto w-full">
                <Outlet />
            </main>
        </div>
    );
}

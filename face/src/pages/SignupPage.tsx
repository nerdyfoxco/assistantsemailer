import { SignupForm } from '../features/auth/SignupForm';

export function SignupPage() {
    return (
        <div className="min-h-screen bg-neutral-100 flex flex-col items-center justify-center p-4">
            <div className="mb-8 text-center">
                <h1 className="text-3xl font-bold text-slate-800">Spine + Face</h1>
                <p className="text-slate-500">Join the Platform</p>
            </div>
            <SignupForm />
        </div>
    );
}

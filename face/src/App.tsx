import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginForm } from './features/auth/LoginForm';
import { DashboardPage } from './pages/DashboardPage';
import { SignupPage } from './pages/SignupPage';

// Simple Auth Guard (Mock) - In real app, check context/redux/api
function RequireAuth({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={
          <div className="min-h-screen bg-neutral-100 flex flex-col items-center justify-center p-4">
            <div className="mb-8 text-center">
              <h1 className="text-3xl font-bold text-slate-800">Spine + Face</h1>
              <p className="text-slate-500">Frontend Integration Demo</p>
            </div>
            <LoginForm />
          </div>
        } />

        <Route path="/signup" element={<SignupPage />} />

        <Route path="/dashboard" element={
          <RequireAuth>
            <DashboardPage />
          </RequireAuth>
        } />

        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

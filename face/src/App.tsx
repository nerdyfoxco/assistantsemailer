import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './features/auth/LoginForm';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { DashboardPage } from './pages/DashboardPage';
import { GoogleCallbackPage } from './pages/GoogleCallbackPage';
import { SignupPage } from './features/auth/SignupPage';
import { InboxView } from './chapters/05_intelligence/InboxView';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/auth/google/callback" element={<GoogleCallbackPage />} />

        {/* Protected Dashboard Routes */}
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          {/* New Intelligence Route (Chapter 5) */}
          <Route path="intelligence" element={<InboxView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

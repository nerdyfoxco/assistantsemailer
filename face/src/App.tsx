import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { DashboardPage } from './pages/DashboardPage';
import { GoogleCallbackPage } from './pages/GoogleCallbackPage';
import { SignupPage } from './pages/SignupPage';
import { InboxView } from './chapters/05_intelligence/InboxView';
import { MindProvider } from './chapters/08_mind/MindContext';
import { HitlDashboard } from './chapters/09_hitl/HitlDashboard';
import { AdminDashboard } from './chapters/10_admin/AdminDashboard';

import { LandingPage } from './chapters/11_gateway/LandingPage';
import { Onboarding } from './chapters/11_gateway/Onboarding';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Gateway Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/security" element={<SecurityPage />} />

        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<Onboarding />} />
        <Route path="/auth/google/callback" element={<GoogleCallbackPage />} />

        {/* Protected Dashboard Routes */}
        <Route path="/app" element={<DashboardLayout />}>
          <Route index element={<Navigate to="/app/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          {/* New Intelligence Route (Chapter 5) */}
          <Route path="intelligence" element={
            <MindProvider>
              <InboxView />
            </MindProvider>
          } />

          {/* HITL Dashboard (Chapter 9) */}
          <Route path="hitl" element={<HitlDashboard />} />

          {/* Admin Dashboard (Chapter 10) */}
          <Route path="admin" element={<AdminDashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

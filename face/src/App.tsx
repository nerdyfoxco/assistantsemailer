import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { DashboardPage } from './pages/DashboardPage';
import { GoogleCallbackPage } from './pages/GoogleCallbackPage';
import { SignupPage } from './pages/SignupPage';
import { InboxView } from './chapters/05_intelligence/InboxView';
import { MindProvider } from './chapters/08_mind/MindContext';

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
          <Route path="intelligence" element={
            <MindProvider>
              <InboxView />
            </MindProvider>
          } />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

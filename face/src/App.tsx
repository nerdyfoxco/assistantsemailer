import { LoginForm } from './features/auth/LoginForm'

function App() {
  return (
    <div className="min-h-screen bg-neutral-100 flex flex-col items-center justify-center p-4">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-slate-800">Spine + Face</h1>
        <p className="text-slate-500">Frontend Integration Demo</p>
      </div>
      <LoginForm />
    </div>
  )
}

export default App

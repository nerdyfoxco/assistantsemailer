import { useState } from 'react'
import { cn } from './lib/utils'
import { Check, Mail } from 'lucide-react'

function App() {
  const [active, setActive] = useState(false)

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-primary">Design System</h1>
          <p className="mt-2 text-muted-foreground">Tailwind + Shadcn Variables</p>
        </div>

        <div className="grid gap-4">
          <div className="p-6 bg-card rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold">Card Component</h3>
            <p className="text-sm text-muted-foreground mt-1">
              This card uses the design system variables for background, border, and text.
            </p>
          </div>

          <div className="flex gap-4 justify-center">
            <button
              className={cn(
                "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
                "bg-primary text-primary-foreground shadow hover:bg-primary/90",
                "h-9 px-4 py-2"
              )}
            >
              Primary Button
            </button>
            <button
              className={cn(
                "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
                "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
                "h-9 px-4 py-2"
              )}
              onClick={() => setActive(!active)}
            >
              {active ? <Check className="mr-2 h-4 w-4" /> : <Mail className="mr-2 h-4 w-4" />}
              Toggle Icon
            </button>
          </div>

          <div className="p-4 rounded-md bg-secondary text-secondary-foreground text-center text-sm">
            Secondary Background Setup Complete
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

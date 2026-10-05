import React from 'react';
import { Activity, ShieldAlert, Cpu } from 'lucide-react';

function App() {
  return (
    <div className="min-h-screen bg-background text-textMain flex flex-col font-sans">
      <header className="h-16 border-b border-border bg-surface flex items-center px-6">
        <Cpu className="text-primary mr-3" />
        <h1 className="text-xl font-semibold tracking-wide">MissionTrace</h1>
        <div className="ml-auto flex items-center space-x-3 text-sm text-textMuted">
          <Activity size={16} />
          <span className="uppercase tracking-wider">System: Ready</span>
        </div>
      </header>

      <main className="flex-1 p-6 flex gap-6">
        <aside className="w-80 flex flex-col gap-6">
          <div className="bg-surface border border-border p-4 rounded bg-opacity-70">
            <h2 className="text-sm font-semibold uppercase text-textMuted mb-4">Query Mission</h2>
            <input 
              type="text" 
              placeholder="Why did BATT_V_A drop around 04:12Z?"
              className="w-full bg-background border border-border p-2 focus:border-primary focus:outline-none rounded text-sm text-textMain"
              disabled
            />
            <p className="text-xs text-textMuted mt-2">(UI Placeholder)</p>
          </div>
        </aside>

        <section className="flex-1 bg-surface border border-border rounded p-6 bg-opacity-70 flex flex-col items-center justify-center text-textMuted">
          <ShieldAlert size={48} className="mb-4 opacity-50" />
          <h2 className="text-xl">Awaiting Query</h2>
          <p className="mt-2 max-w-md text-center text-sm">
            MissionTrace will retrieve correlated telemetry, analyze incidents, and output evidence-grounded findings.
          </p>
        </section>
      </main>
    </div>
  );
}

export default App;

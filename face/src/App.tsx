import { useEffect, useState } from 'react';
import { api } from './lib/api';
import type { WorkItem } from './lib/types';
import { cn } from './lib/utils';
import { Loader2, CheckCircle, Brain, RefreshCcw } from 'lucide-react';

function App() {
  const [items, setItems] = useState<WorkItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Poll for updates (Simple Real-time)
  useEffect(() => {
    const fetchItems = () => api.listItems().then(setItems).catch(console.error);
    fetchItems();
    const interval = setInterval(fetchItems, 2000);
    return () => clearInterval(interval);
  }, []);

  const selectedItem = items.find(i => i.id === selectedId);

  const handleDraft = async (id: string) => {
    setLoading(true);
    try {
      await api.triggerDraft(id);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: string) => {
    setLoading(true);
    try {
      await api.approveDraft(id);
      setSelectedId(null); // Deselect on success
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 font-sans">
      {/* Sidebar: Inbox */}
      <div className="w-1/3 border-r border-gray-800 p-4 overflow-y-auto">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <RefreshCcw className="w-5 h-5" /> Inbox
        </h2>
        <div className="space-y-2">
          {items.map(item => (
            <div
              key={item.id}
              onClick={() => setSelectedId(item.id)}
              className={cn(
                "p-3 rounded-lg cursor-pointer border transition-colors",
                selectedId === item.id
                  ? "bg-gray-800 border-blue-500"
                  : "bg-gray-800/50 border-gray-700 hover:bg-gray-800"
              )}
            >
              <div className="flex justify-between items-center mb-1">
                <span className={cn(
                  "text-xs px-2 py-0.5 rounded-full font-medium",
                  item.state === 'NEW' ? "bg-blue-900 text-blue-200" :
                    item.state === 'REVIEW' ? "bg-amber-900 text-amber-200" :
                      item.state === 'CLOSED' ? "bg-green-900 text-green-200" :
                        "bg-gray-700"
                )}>
                  {item.state}
                </span>
                <span className="text-xs text-gray-500">{item.id.slice(0, 8)}</span>
              </div>
              <div className="text-sm text-gray-300 truncate">
                Message ID: {item.source_message_id}
              </div>
            </div>
          ))}
          {items.length === 0 && (
            <div className="text-center text-gray-500 py-10">No items found</div>
          )}
        </div>
      </div>

      {/* Main: Workspace */}
      <div className="flex-1 p-8 flex flex-col">
        {selectedItem ? (
          <div className="max-w-2xl mx-auto w-full space-y-6">

            {/* Context Widget */}
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-xl">
              <h3 className="text-lg font-semibold mb-2 text-gray-200">Processing Item</h3>
              <div className="grid grid-cols-2 gap-4 text-sm text-gray-400">
                <div>Tenant: {selectedItem.tenant_id}</div>
                <div>Source: {selectedItem.source_message_id}</div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex flex-col gap-4">

              {/* Draft Generation */}
              {selectedItem.state === 'NEW' && (
                <button
                  onClick={() => handleDraft(selectedItem.id)}
                  disabled={loading}
                  className="bg-blue-600 hover:bg-blue-500 text-white py-4 rounded-xl font-medium flex items-center justify-center gap-2 transition-all"
                >
                  {loading ? <Loader2 className="animate-spin" /> : <Brain />}
                  Generate Draft
                </button>
              )}

              {/* Review & Approve */}
              {selectedItem.state === 'REVIEW' && selectedItem.draft_context && (
                <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
                  <div className="bg-gray-900/50 p-4 border-b border-gray-700 font-mono text-sm text-gray-400">
                    AI DRAFT ({selectedItem.draft_context.tone})
                  </div>
                  <div className="p-6 text-gray-100 whitespace-pre-wrap font-serif text-lg leading-relaxed">
                    {selectedItem.draft_context.body}
                  </div>
                  <div className="p-4 bg-gray-900/30 flex justify-end">
                    <button
                      onClick={() => handleApprove(selectedItem.id)}
                      disabled={loading}
                      className="bg-green-600 hover:bg-green-500 text-white px-8 py-2 rounded-lg font-medium flex items-center gap-2"
                    >
                      {loading ? <Loader2 className="animate-spin" /> : <CheckCircle />}
                      Approve & Send
                    </button>
                  </div>
                </div>
              )}

              {selectedItem.state === 'CLOSED' && (
                <div className="text-center p-10 text-green-500 font-bold text-xl flex flex-col items-center gap-2">
                  <CheckCircle className="w-10 h-10" />
                  Sent Successfully
                </div>
              )}

            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-600">
            Select an item from the inbox to begin
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

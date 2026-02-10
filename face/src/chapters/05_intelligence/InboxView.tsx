import { useEffect, useState } from 'react';
import type { TriageResult, ProxyResult } from './intelligenceService'; // Type-only import
import { intelligenceService } from './intelligenceService';
import { AlertCircle, Mail, Shield, User, Zap, Paperclip, File } from 'lucide-react';

export function InboxView() {
    const [streamStatus, setStreamStatus] = useState<'idle' | 'streaming' | 'done' | 'error'>('idle');
    const [items, setItems] = useState<TriageResult[]>([]);
    const [selectedId, setSelectedId] = useState<string | null>(null);
    const [bodyLoading, setBodyLoading] = useState(false);
    const [bodyData, setBodyData] = useState<ProxyResult | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    // 1. Start Stream on Mount
    useEffect(() => {
        setStreamStatus('streaming');
        const cleanup = intelligenceService.streamWorkItems(
            (item) => {
                setItems((prev) => {
                    // Avoid creating duplicates if stream restarts or yields same ID
                    if (prev.find(i => i.id === item.id)) return prev;
                    return [...prev, item];
                });
            },
            (err) => {
                console.error("Stream Error", err);
                setStreamStatus('error');
                setErrorMsg(String(err));
            },
            () => {
                setStreamStatus('done');
            }
        );

        return () => cleanup();
    }, []);

    // 2. Fetch Body when Selected
    useEffect(() => {
        if (!selectedId) {
            setBodyData(null);
            return;
        }

        const fetchBody = async () => {
            setBodyLoading(true);
            setBodyData(null);
            try {
                // Use selectedId (which is message_id now)
                const data = await intelligenceService.getMessageBody(selectedId);
                setBodyData(data);
            } catch (err) {
                console.error("Body Fetch Error", err);
                setErrorMsg("Failed to load message body.");
            } finally {
                setBodyLoading(false);
            }
        };

        fetchBody();
    }, [selectedId]);

    const getConfidenceColor = (band: string) => {
        switch (band) {
            case 'HIGH': return 'bg-green-100 text-green-800 border-green-200';
            case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
            case 'LOW': return 'bg-gray-100 text-gray-800 border-gray-200';
            default: return 'bg-gray-100';
        }
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 h-[calc(100vh-4rem)] bg-gray-50 p-4 gap-4">
            {/* Left: Triage List */}
            <div className="md:col-span-1 flex flex-col h-full bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-white sticky top-0 z-10">
                    <h2 className="text-lg font-semibold flex items-center gap-2 text-gray-900">
                        <Zap className="w-5 h-5 text-purple-600" />
                        Live Triage
                    </h2>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${streamStatus === 'streaming' ? 'bg-green-100 text-green-700' :
                        streamStatus === 'error' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'
                        }`}>
                        {streamStatus === 'streaming' ? 'Live Streaming' : streamStatus}
                    </span>
                </div>

                <div className="flex-1 overflow-y-auto p-3 space-y-2">
                    {errorMsg && (
                        <div className="p-3 bg-red-50 border border-red-100 rounded-lg text-sm text-red-600 flex items-center gap-2">
                            <AlertCircle className="w-4 h-4" />
                            {errorMsg}
                        </div>
                    )}

                    {items.length === 0 && streamStatus === 'streaming' && (
                        <div className="space-y-3 animate-pulse">
                            <div className="h-24 bg-gray-100 rounded-lg"></div>
                            <div className="h-24 bg-gray-100 rounded-lg"></div>
                            <div className="h-24 bg-gray-100 rounded-lg"></div>
                        </div>
                    )}

                    {items.map((item) => (
                        <div
                            key={item.id}
                            onClick={() => setSelectedId(item.message_id)}
                            className={`p-3 rounded-lg border cursor-pointer transition-all hover:shadow-md text-left ${selectedId === item.message_id ? 'bg-purple-50 border-purple-200 ring-1 ring-purple-300' : 'bg-white border-gray-100'
                                }`}
                        >
                            <div className="flex justify-between items-start mb-1">
                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getConfidenceColor(item.confidence_band)}`}>
                                    {item.confidence_score}% Cmd
                                </span>
                                {item.is_vip && (
                                    <Shield className="w-3.5 h-3.5 text-amber-500" />
                                )}
                            </div>
                            <h4 className="font-semibold text-gray-900 truncate text-sm mb-0.5">{item.subject || '(No Subject)'}</h4>
                            <div className="flex items-center gap-1 text-xs text-gray-500 mb-2">
                                <User className="w-3 h-3" />
                                <span className="truncate">{item.sender}</span>
                            </div>
                            <div className="flex flex-wrap gap-1">
                                {item.tags.map(tag => (
                                    <span key={tag} className="text-[10px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded border border-gray-200">
                                        #{tag}
                                    </span>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Right: Message View (Proxy) */}
            <div className="md:col-span-2 flex flex-col h-full bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="p-6 border-b border-gray-100 min-h-[5rem] flex flex-col justify-center">
                    {selectedId ? (
                        items.find(i => i.message_id === selectedId) && (
                            <div>
                                <h2 className="text-xl font-bold text-gray-900 leading-tight">
                                    {items.find(i => i.message_id === selectedId)?.subject}
                                </h2>
                                <div className="text-sm text-gray-500 mt-1 flex items-center gap-2">
                                    <span className="font-medium text-gray-700">{items.find(i => i.message_id === selectedId)?.sender}</span>
                                    <span className="text-gray-300">|</span>
                                    <span>{items.find(i => i.message_id === selectedId)?.received_at}</span>
                                </div>
                            </div>
                        )
                    ) : (
                        <div className="text-gray-400 font-medium flex items-center gap-2">
                            <Mail className="w-5 h-5" />
                            Select an item to view body
                        </div>
                    )}
                </div>

                <div className="flex-1 overflow-y-auto bg-white p-6">
                    {bodyLoading ? (
                        <div className="space-y-4 animate-pulse">
                            <div className="h-4 w-3/4 bg-gray-100 rounded"></div>
                            <div className="h-4 w-1/2 bg-gray-100 rounded"></div>
                            <div className="h-64 w-full bg-gray-100 rounded"></div>
                        </div>
                    ) : bodyData ? (
                        <div className="prose prose-sm max-w-none text-gray-800">
                            {/* DANGEROUSLY SET HTML (Sanitized by Backend Bleach) */}
                            <div dangerouslySetInnerHTML={{ __html: bodyData.html }} />

                            {/* Attachments Section */}
                            {bodyData.attachments && bodyData.attachments.length > 0 && (
                                <div className="mt-8 pt-4 border-t border-gray-100">
                                    <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                                        <Paperclip className="w-3.5 h-3.5" />
                                        Attachments ({bodyData.attachments.length})
                                    </h4>
                                    <div className="flex flex-wrap gap-2">
                                        {bodyData.attachments.map((att, idx) => (
                                            <div key={idx} className="group flex items-center gap-3 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg hover:border-purple-200 hover:bg-purple-50 transition-colors cursor-default">
                                                <div className="p-1.5 bg-white rounded border border-gray-100 group-hover:border-purple-100">
                                                    <File className="w-4 h-4 text-blue-500" />
                                                </div>
                                                <div className="flex flex-col">
                                                    <span className="text-sm font-medium text-gray-700 max-w-[180px] truncate" title={att.filename}>
                                                        {att.filename}
                                                    </span>
                                                    <span className="text-[10px] text-gray-400">
                                                        {Math.round((att.size || 0) / 1024)} KB • {att.mime_type?.split('/')[1] || 'file'}
                                                    </span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        !selectedId && (
                            <div className="flex flex-col items-center justify-center h-full text-gray-300">
                                <Zap className="w-16 h-16 mb-4 opacity-20" />
                                <p>Live Proxy Ready</p>
                            </div>
                        )
                    )}
                </div>
            </div>
        </div>
    );
}

'use client'

import { useState, useEffect, useRef } from 'react'
import { Send, BookOpen, Sparkles, RotateCcw } from 'lucide-react'
import { Navigation } from '@/components/navigation'

interface Message {
    role: 'user' | 'assistant'
    content: string
    sources?: Array<{
        content: string
        source: string
        category: string
    }>
}

export default function AskGTMPage() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const [stats, setStats] = useState<any>(null)
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    useEffect(() => {
        fetchStats()
    }, [])

    const fetchStats = async () => {
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/askgtm/stats`)
            const data = await res.json()
            setStats(data)
        } catch (error) {
            console.error('Error fetching stats:', error)
        }
    }

    const handleSend = async () => {
        if (!input.trim() || loading) return

        const userMessage: Message = { role: 'user', content: input }
        setMessages(prev => [...prev, userMessage])
        setInput('')
        setLoading(true)

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/askgtm/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: input }),
            })

            const data = await res.json()

            const assistantMessage: Message = {
                role: 'assistant',
                content: data.answer,
                sources: data.sources,
            }

            setMessages(prev => [...prev, assistantMessage])
        } catch (error) {
            console.error('Error:', error)
            const errorMessage: Message = {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.',
            }
            setMessages(prev => [...prev, errorMessage])
        } finally {
            setLoading(false)
        }
    }

    const handleReset = async () => {
        try {
            await fetch(`${process.env.NEXT_PUBLIC_API_URL}/askgtm/reset`, {
                method: 'POST',
            })
            setMessages([])
        } catch (error) {
            console.error('Error resetting:', error)
        }
    }

    const exampleQuestions = [
        "What's our pricing for enterprise customers?",
        "How do we handle the 'too expensive' objection?",
        "What are our key differentiators vs Clari?",
        "What's included in the Professional plan?",
        "How long is implementation?",
    ]

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-900 to-purple-800 p-4">
            <div className="max-w-5xl mx-auto h-screen flex flex-col">
                <Navigation />
                {/* Header */}
                <div className="py-6 px-4 bg-white/10 backdrop-blur-lg rounded-t-xl">
                    <div className="flex justify-between items-center">
                        <div>
                            <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                                <BookOpen size={32} />
                                AskGTM AI
                            </h1>
                            <p className="text-purple-200">Your AI-powered GTM knowledge assistant</p>
                        </div>
                        <div className="text-right">
                            {stats && (
                                <div className="text-white/80 text-sm">
                                    <div>{stats.total_documents} documents</div>
                                    <div>{stats.categories?.length || 0} categories</div>
                                </div>
                            )}
                            <button
                                onClick={handleReset}
                                className="mt-2 text-white/60 hover:text-white flex items-center gap-1 text-sm"
                            >
                                <RotateCcw size={16} />
                                Reset Chat
                            </button>
                        </div>
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto bg-white/5 backdrop-blur-lg p-6 space-y-4">
                    {messages.length === 0 && (
                        <div className="text-center py-12">
                            <Sparkles className="mx-auto mb-4 text-purple-300" size={48} />
                            <h2 className="text-2xl font-bold text-white mb-4">Ask me anything about GTM</h2>
                            <p className="text-purple-200 mb-6">Try one of these questions:</p>
                            <div className="space-y-2 max-w-2xl mx-auto">
                                {exampleQuestions.map((q, idx) => (
                                    <button
                                        key={idx}
                                        onClick={() => setInput(q)}
                                        className="block w-full text-left px-4 py-3 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
                                    >
                                        {q}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {messages.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-3xl rounded-2xl p-4 ${msg.role === 'user'
                                        ? 'bg-purple-600 text-white'
                                        : 'bg-white text-slate-800'
                                    }`}
                            >
                                <div className="whitespace-pre-wrap">{msg.content}</div>

                                {msg.sources && msg.sources.length > 0 && (
                                    <div className="mt-4 pt-4 border-t border-slate-200">
                                        <p className="text-sm font-semibold mb-2 text-slate-600">Sources:</p>
                                        <div className="space-y-2">
                                            {msg.sources.map((source, sidx) => (
                                                <div key={sidx} className="text-xs bg-slate-50 p-2 rounded">
                                                    <div className="font-semibold text-slate-700">
                                                        {source.source} ({source.category})
                                                    </div>
                                                    <div className="text-slate-600">{source.content}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-white rounded-2xl p-4">
                                <div className="flex gap-2">
                                    <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" />
                                    <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce delay-100" />
                                    <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce delay-200" />
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="p-4 bg-white/10 backdrop-blur-lg rounded-b-xl">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask about pricing, objections, features, competitors..."
                            className="flex-1 px-4 py-3 rounded-lg bg-white/90 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                            disabled={loading}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || loading}
                            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send size={20} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
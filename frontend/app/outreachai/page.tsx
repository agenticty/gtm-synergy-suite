'use client'

import { useState } from 'react'
import { Mail, Linkedin, MessageSquare, Sparkles, Copy, Check } from 'lucide-react'
import { Navigation } from '@/components/navigation'

interface OutreachResult {
    subject: string
    body: string
    reasoning: string
    personalization_elements: string[]
    call_to_action: string
}

export default function OutreachAIPage() {
    const [formData, setFormData] = useState({
        company_name: '',
        industry: '',
        company_size: '',
        pain_points: '',
        decision_maker_name: '',
        decision_maker_title: '',
        recent_activity: '',
        channel: 'email',
    })

    const [result, setResult] = useState<OutreachResult | null>(null)
    const [loading, setLoading] = useState(false)
    const [copied, setCopied] = useState(false)

    const channels = [
        { id: 'email', name: 'Email', icon: Mail, color: 'blue' },
        { id: 'linkedin', name: 'LinkedIn', icon: Linkedin, color: 'indigo' },
        { id: 'slack', name: 'Slack', icon: MessageSquare, color: 'purple' },
    ]

    const handleGenerate = async () => {
        setLoading(true)

        try {
            const payload = {
                ...formData,
                pain_points: formData.pain_points.split(',').map(p => p.trim()).filter(Boolean),
            }

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/outreachai/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            })

            const data = await res.json()
            setResult(data)
        } catch (error) {
            console.error('Error:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleCopy = () => {
        if (!result) return

        const text = result.subject
            ? `Subject: ${result.subject}\n\n${result.body}`
            : result.body

        navigator.clipboard.writeText(text)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    const isFormValid = () => {
        return formData.company_name && formData.industry && formData.company_size && formData.pain_points
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-900 to-indigo-800 p-8">
            <div className="max-w-7xl mx-auto">
                <Navigation />
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
                        <Sparkles size={40} />
                        OutreachAI
                    </h1>
                    <p className="text-indigo-200">AI-powered personalized outreach generation</p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Input Form */}
                    <div className="bg-white rounded-xl p-8 shadow-xl">
                        <h2 className="text-2xl font-bold mb-6">Prospect Information</h2>

                        {/* Channel Selection */}
                        <div className="mb-6">
                            <label className="block text-sm font-semibold mb-3">Channel</label>
                            <div className="grid grid-cols-3 gap-3">
                                {channels.map(channel => {
                                    const Icon = channel.icon
                                    const isSelected = formData.channel === channel.id

                                    return (
                                        <button
                                            key={channel.id}
                                            onClick={() => setFormData({ ...formData, channel: channel.id })}
                                            className={`p-4 rounded-lg border-2 transition-all ${isSelected
                                                    ? `border-${channel.color}-600 bg-${channel.color}-50`
                                                    : 'border-gray-200 hover:border-gray-300'
                                                }`}
                                        >
                                            <Icon className={`mx-auto mb-2 ${isSelected ? `text-${channel.color}-600` : 'text-gray-400'}`} size={24} />
                                            <div className={`text-sm font-medium ${isSelected ? `text-${channel.color}-600` : 'text-gray-600'}`}>
                                                {channel.name}
                                            </div>
                                        </button>
                                    )
                                })}
                            </div>
                        </div>

                        {/* Company Info */}
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-semibold mb-2">Company Name *</label>
                                <input
                                    type="text"
                                    value={formData.company_name}
                                    onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                                    placeholder="Acme Corp"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Industry *</label>
                                    <input
                                        type="text"
                                        value={formData.industry}
                                        onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                                        placeholder="SaaS"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold mb-2">Company Size *</label>
                                    <input
                                        type="text"
                                        value={formData.company_size}
                                        onChange={(e) => setFormData({ ...formData, company_size: e.target.value })}
                                        placeholder="50-200"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-semibold mb-2">Pain Points * (comma-separated)</label>
                                <textarea
                                    value={formData.pain_points}
                                    onChange={(e) => setFormData({ ...formData, pain_points: e.target.value })}
                                    placeholder="manual processes, poor pipeline visibility, low conversion rates"
                                    rows={3}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Decision Maker Name</label>
                                    <input
                                        type="text"
                                        value={formData.decision_maker_name}
                                        onChange={(e) => setFormData({ ...formData, decision_maker_name: e.target.value })}
                                        placeholder="Jane Smith"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold mb-2">Title</label>
                                    <input
                                        type="text"
                                        value={formData.decision_maker_title}
                                        onChange={(e) => setFormData({ ...formData, decision_maker_title: e.target.value })}
                                        placeholder="VP Sales"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-semibold mb-2">Recent Activity</label>
                                <textarea
                                    value={formData.recent_activity}
                                    onChange={(e) => setFormData({ ...formData, recent_activity: e.target.value })}
                                    placeholder="Visited pricing page 3x, downloaded case study..."
                                    rows={2}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                />
                            </div>

                            <button
                                onClick={handleGenerate}
                                disabled={!isFormValid() || loading}
                                className="w-full py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                {loading ? 'Generating...' : 'Generate Outreach'}
                            </button>
                        </div>
                    </div>

                    {/* Output */}
                    <div className="bg-white rounded-xl p-8 shadow-xl">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-2xl font-bold">Generated Outreach</h2>
                            {result && (
                                <button
                                    onClick={handleCopy}
                                    className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                                >
                                    {copied ? (
                                        <>
                                            <Check size={16} className="text-green-600" />
                                            <span className="text-sm text-green-600">Copied!</span>
                                        </>
                                    ) : (
                                        <>
                                            <Copy size={16} />
                                            <span className="text-sm">Copy</span>
                                        </>
                                    )}
                                </button>
                            )}
                        </div>

                        {!result && !loading && (
                            <div className="text-center py-12 text-gray-400">
                                <Sparkles className="mx-auto mb-4" size={48} />
                                <p>Fill in the form and click generate to create personalized outreach</p>
                            </div>
                        )}

                        {loading && (
                            <div className="text-center py-12">
                                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
                                <p className="text-gray-600">AI agents are crafting your perfect outreach...</p>
                            </div>
                        )}

                        {result && (
                            <div className="space-y-6">
                                {/* Subject (if email) */}
                                {result.subject && (
                                    <div>
                                        <label className="block text-sm font-semibold mb-2 text-gray-600">Subject Line</label>
                                        <div className="p-4 bg-indigo-50 rounded-lg">
                                            <p className="font-semibold text-indigo-900">{result.subject}</p>
                                        </div>
                                    </div>
                                )}

                                {/* Body */}
                                <div>
                                    <label className="block text-sm font-semibold mb-2 text-gray-600">Message</label>
                                    <div className="p-4 bg-gray-50 rounded-lg">
                                        <p className="whitespace-pre-wrap text-gray-800">{result.body}</p>
                                    </div>
                                </div>

                                {/* Personalization Elements */}
                                <div>
                                    <label className="block text-sm font-semibold mb-2 text-gray-600">Personalization Elements</label>
                                    <div className="flex flex-wrap gap-2">
                                        {result.personalization_elements.map((element, idx) => (
                                            <span
                                                key={idx}
                                                className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm"
                                            >
                                                {element}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                {/* Reasoning */}
                                <div>
                                    <label className="block text-sm font-semibold mb-2 text-gray-600">AI Reasoning</label>
                                    <div className="p-4 bg-yellow-50 rounded-lg">
                                        <p className="text-sm text-gray-700">{result.reasoning}</p>
                                    </div>
                                </div>

                                {/* CTA */}
                                <div>
                                    <label className="block text-sm font-semibold mb-2 text-gray-600">Call to Action</label>
                                    <div className="p-3 bg-blue-50 rounded-lg">
                                        <p className="text-blue-900 font-medium">{result.call_to_action}</p>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
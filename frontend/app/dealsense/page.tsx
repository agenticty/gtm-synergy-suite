'use client'

import { useState } from 'react'
import { Upload } from 'lucide-react'
import { Navigation } from '@/components/navigation'

interface DealScore {
    deal_id: string
    company_name: string
    deal_value: number
    close_probability: number
    risk_level: string
    reasoning: string
    next_actions: string[]
}

export default function DealSensePage() {
    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState<DealScore[]>([])

    const handleUpload = async () => {
        if (!file) return

        setLoading(true)
        const formData = new FormData()
        formData.append('file', file)

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/dealsense/analyze-csv`, {
                method: 'POST',
                body: formData,
            })

            const data = await res.json()
            setResults(data)
        } catch (error) {
            console.error('Error:', error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8">
            <div className="max-w-7xl mx-auto">
                <Navigation />
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-white mb-2">DealSense AI</h1>
                    <p className="text-slate-300">Pipeline forecasting + AI deal scoring</p>
                </div>

                {/* Upload Section */}
                <div className="bg-white rounded-xl p-8 shadow-xl mb-8">
                    <div className="border-2 border-dashed border-slate-300 rounded-lg p-12 text-center">
                        <Upload className="mx-auto mb-4 text-slate-400" size={48} />
                        <p className="text-lg mb-4">Upload your deals CSV</p>
                        <input
                            type="file"
                            accept=".csv"
                            onChange={(e) => setFile(e.target.files?.[0] || null)}
                            className="mb-4"
                        />
                        <button
                            onClick={handleUpload}
                            disabled={!file || loading}
                            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                        >
                            {loading ? 'Analyzing...' : 'Analyze Pipeline'}
                        </button>
                    </div>
                </div>

                {/* Results */}
                {results.length > 0 && (
                    <div className="space-y-4">
                        {results.map((deal) => (
                            <div key={deal.deal_id} className="bg-white rounded-lg p-6 shadow-lg">
                                <div className="flex justify-between items-start mb-4">
                                    <div>
                                        <h3 className="text-xl font-bold">{deal.company_name}</h3>
                                        <p className="text-slate-600">${deal.deal_value.toLocaleString()}</p>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-3xl font-bold text-green-600">
                                            {deal.close_probability}%
                                        </div>
                                        <div className={`text-sm font-semibold ${deal.risk_level === 'High' ? 'text-red-600' :
                                                deal.risk_level === 'Medium' ? 'text-yellow-600' :
                                                    'text-green-600'
                                            }`}>
                                            {deal.risk_level} Risk
                                        </div>
                                    </div>
                                </div>

                                <div className="mb-4">
                                    <p className="text-slate-700">{deal.reasoning}</p>
                                </div>

                                <div>
                                    <h4 className="font-semibold mb-2">Next Actions:</h4>
                                    <ul className="list-disc list-inside space-y-1">
                                        {deal.next_actions.map((action, idx) => (
                                            <li key={idx} className="text-slate-600">{action}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
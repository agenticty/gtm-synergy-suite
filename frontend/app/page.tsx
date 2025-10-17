'use client'

import Link from 'next/link'
import { TrendingUp, BookOpen, Sparkles, ArrowRight } from 'lucide-react'

export default function DashboardPage() {
  const tools = [
    {
      id: 'dealsense',
      name: 'DealSense AI',
      description: 'Pipeline forecasting + AI deal scoring',
      icon: TrendingUp,
      color: 'from-blue-600 to-blue-700',
      href: '/dealsense',
      features: ['Deal probability scoring', 'Risk detection', 'Next-best actions']
    },
    {
      id: 'askgtm',
      name: 'AskGTM AI',
      description: 'RAG-powered GTM knowledge assistant',
      icon: BookOpen,
      color: 'from-purple-600 to-purple-700',
      href: '/askgtm',
      features: ['Instant answers', 'Source citations', 'Conversation memory']
    },
    {
      id: 'outreachai',
      name: 'OutreachAI',
      description: 'Multi-channel engagement automation',
      icon: Sparkles,
      color: 'from-indigo-600 to-indigo-700',
      href: '/outreachai',
      features: ['Personalized outreach', 'Multi-channel', 'A/B testing']
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="border-b border-white/10 backdrop-blur-lg bg-white/5">
        <div className="max-w-7xl mx-auto px-8 py-6">
          <h1 className="text-4xl font-bold text-white">GTM Synergy Suite</h1>
          <p className="text-slate-300 mt-2">AI-powered tools for GTM teams</p>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-white mb-4">
            Supercharge Your GTM Operations
          </h2>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Three AI-powered tools that automate pipeline forecasting, knowledge retrieval,
            and personalized outreach—saving your team 10+ hours per week.
          </p>
        </div>

        {/* Tools Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {tools.map((tool) => {
            const Icon = tool.icon

            return (
              <Link
                key={tool.id}
                href={tool.href}
                className="group relative bg-white/10 backdrop-blur-lg rounded-2xl p-8 hover:bg-white/15 transition-all duration-300 border border-white/10 hover:border-white/20 hover:scale-105"
              >
                <div className={`inline-flex p-4 rounded-xl bg-gradient-to-br ${tool.color} mb-6`}>
                  <Icon className="text-white" size={32} />
                </div>

                <h3 className="text-2xl font-bold text-white mb-2">{tool.name}</h3>
                <p className="text-slate-300 mb-6">{tool.description}</p>

                <ul className="space-y-2 mb-6">
                  {tool.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-slate-400 text-sm">
                      <div className="w-1.5 h-1.5 rounded-full bg-green-400 mr-2"></div>
                      {feature}
                    </li>
                  ))}
                </ul>

                <div className="flex items-center text-white font-semibold group-hover:gap-3 gap-2 transition-all">
                  Open Tool
                  <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            )
          })}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-8 border border-white/10">
            <div className="text-4xl font-bold text-white mb-2">80%</div>
            <div className="text-slate-300">Reduction in manual work</div>
          </div>
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-8 border border-white/10">
            <div className="text-4xl font-bold text-white mb-2">10+</div>
            <div className="text-slate-300">Hours saved per week</div>
          </div>
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-8 border border-white/10">
            <div className="text-4xl font-bold text-white mb-2">3x</div>
            <div className="text-slate-300">Faster deal qualification</div>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="bg-white/5 backdrop-blur-lg rounded-xl p-8 border border-white/10">
          <h3 className="text-xl font-bold text-white mb-4">Built With</h3>
          <div className="flex flex-wrap gap-3">
            {['Python', 'FastAPI', 'LangChain', 'CrewAI', 'Next.js', 'OpenAI', 'ChromaDB'].map((tech) => (
              <span
                key={tech}
                className="px-4 py-2 bg-white/10 rounded-lg text-slate-200 text-sm font-medium"
              >
                {tech}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-white/10 mt-16">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <p className="text-center text-slate-400">
            GTM Synergy Suite • Built by{' '}
            <a
              href="https://github.com/agenticty"
              target="_blank"
              rel="noopener noreferrer"
              className="text-white hover:underline"
            >
              @agenticty
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}
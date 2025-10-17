import Link from 'next/link'
import { Home, ArrowLeft } from 'lucide-react'

export function Navigation() {
    return (
        <div className="mb-8">
            <Link
                href="/"
                className="inline-flex items-center gap-2 text-white/80 hover:text-white transition-colors"
            >
                <ArrowLeft size={20} />
                Back to Dashboard
            </Link>
        </div>
    )
}
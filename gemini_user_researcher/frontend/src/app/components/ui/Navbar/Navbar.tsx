'use client';

import Link from 'next/link';

export const Navbar = () => {
    return (
      <nav className="bg-navy border-b border-navy-light">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo/Brand */}
            <div className="flex-shrink-0">
                <Link href="/" className="text-2xl font-bold text-neutral-50 hover:text-sand transition-colors">
                    UI Insight
                </Link>
            </div>

            {/* Navigation Links */}
            <div className="flex space-x-4">
                <Link 
                    href="/"
                    className="px-4 py-2 rounded-lg text-neutral-50 hover:bg-navy-light transition-colors"
                >
                    WCAG Analysis
                </Link>
                <Link 
                    href="/"
                    className="px-4 py-2 rounded-lg text-neutral-50 hover:bg-navy-light transition-colors"
                >
                    Usability Testing
                </Link>
            </div>
          </div>
        </div>
      </nav>
    );
};
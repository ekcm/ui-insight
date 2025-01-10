'use client';

import { useState } from 'react';

export const InputWebLink = () => {
    const [url, setUrl] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Handle URL submission here
        console.log('Submitted URL:', url);
    };

    return (
        <div className="max-w-2xl mx-auto p-4">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter website URL"
                    className="w-full px-4 py-2 rounded-lg border border-navy-light bg-navy text-neutral-50 placeholder-neutral-400 focus:outline-none focus:border-sand"
                    required
                />
                <button
                    type="submit"
                    className="px-6 py-2 bg-sand text-navy font-semibold rounded-lg hover:bg-sand-light transition-colors"
                >
                    Analyze Website
                </button>
            </form>
        </div>
    );
};

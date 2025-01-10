'use client';

import { useState } from 'react';

interface WCAGIssue {
    guideline: string;
    issue: string;
}

interface AnalysisResponse {
    wcag_analysis: WCAGIssue[];
    usability_insights: string[];
    recommendations: string[];
}

export const InputWebLink = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setAnalysis(null);

        try {
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            if (!response.ok) {
                throw new Error('Failed to analyze website');
            }

            const data: AnalysisResponse = await response.json();
            setAnalysis(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-4">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter website URL"
                    className="w-full px-4 py-2 rounded-lg border border-navy-light bg-navy text-neutral-50 placeholder-neutral-400 focus:outline-none focus:border-sand"
                    required
                    disabled={loading}
                />
                <button
                    type="submit"
                    className="px-6 py-2 bg-sand text-navy font-semibold rounded-lg hover:bg-sand-light transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={loading}
                >
                    {loading ? 'Analyzing...' : 'Analyze Website'}
                </button>
            </form>

            {error && (
                <div className="mt-4 p-4 bg-red-500 text-white rounded-lg">
                    {error}
                </div>
            )}

            {analysis && (
                <div className="mt-8 space-y-8">
                    {analysis.wcag_analysis.length > 0 && (
                        <section>
                            <h2 className="text-2xl font-bold text-neutral-50 mb-4">WCAG Analysis</h2>
                            <div className="grid grid-cols-1 gap-4">
                                {analysis.wcag_analysis.map((item, index) => (
                                    <div key={index} className="p-6 bg-navy rounded-lg border border-navy-light hover:border-sand transition-colors">
                                        <h3 className="text-lg font-semibold text-sand mb-2">{item.guideline}</h3>
                                        <p className="text-neutral-300">{item.issue}</p>
                                    </div>
                                ))}
                            </div>
                        </section>
                    )}

                    {analysis.usability_insights.length > 0 && (
                        <section>
                            <h2 className="text-2xl font-bold text-neutral-50 mb-4">Usability Insights</h2>
                            <div className="grid grid-cols-1 gap-4">
                                {analysis.usability_insights.map((insight, index) => (
                                    <div key={index} className="p-6 bg-teal rounded-lg border border-navy-light hover:border-sand transition-colors">
                                        <p className="text-neutral-300">{insight}</p>
                                    </div>
                                ))}
                            </div>
                        </section>
                    )}

                    {analysis.recommendations.length > 0 && (
                        <section>
                            <h2 className="text-2xl font-bold text-neutral-50 mb-4">Recommendations</h2>
                            <div className="grid grid-cols-1 gap-4">
                                {analysis.recommendations.map((recommendation, index) => (
                                    <div key={index} className="p-6 bg-sage-dark rounded-lg border border-navy-light hover:border-sand transition-colors">
                                        <p className="text-neutral-300">{recommendation}</p>
                                    </div>
                                ))}
                            </div>
                        </section>
                    )}

                    {analysis.wcag_analysis.length === 0 && 
                     analysis.usability_insights.length === 0 && 
                     analysis.recommendations.length === 0 && (
                        <div className="text-center text-neutral-300 p-6 bg-navy rounded-lg border border-navy-light">
                            No issues found. The website appears to follow good accessibility and usability practices.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

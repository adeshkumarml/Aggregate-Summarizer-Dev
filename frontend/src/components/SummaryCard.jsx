import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

function SummaryCard({ title, subtitle, summary, metrics, isConsolidated = false }) {
    const [showMetrics, setShowMetrics] = useState(false);
    const metricLabels = {
        semantic_sim: "Semantic Similarity",
        coverage_score: "Coverage Score",
        compression_ratio: "Compression Ratio",
        latency_secs: "Latency (seconds)",
        total_tokens: "Total Tokens",
        estimated_cost: "Estimated Cost (USD)",
        agreement_score: "Agreement Score",
        participating_models: "Participating Models"
    };
    const formatMetric = (key, value) => {
        switch (key) {
            case "semantic_sim":
            case "coverage_score":
            case "agreement_score":
                return `${(value * 100).toFixed(1)}%`;

            case "compression_ratio":
                return `${value.toFixed(2)}×`;

            case "latency_secs":
                return `${value.toFixed(2)} s`;

            case "estimated_cost":
                return `$${value.toFixed(6)}`;

            case "total_tokens":
                return value.toLocaleString();

            default:
                return value;
        }
    };

    return (
        <section className={`mt-8 rounded-2xl bg-white p-6 md:p-8 ${isConsolidated ? "border-2 border-blue-200" : "border border-gray-300"}`}>
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <h3 className={`text-xl font-semibold md:text-2xl ${isConsolidated ? "text-blue-600" : "text-gray-400"}`}>{title}</h3>
                    {isConsolidated && ( <p className="mt-1 text-sm text-gray-500">{subtitle}</p> )}
                </div>
            </div>
            
            <div className="mt-6 max-h-[450px] overflow-y-auto rounded-xl border border-gray-200 bg-gray-200 p-5">
                <p className="whitespace-pre-wrap leading-7 text-gray-800">{summary}</p>
            </div>

            <div className="mt-6">
                <button onClick={() => setShowMetrics(!showMetrics)} className="flex items-center gap-2 text-sm font-medium text-blue-600 transition hover:text-blue-700">
                    {showMetrics ? (
                        <>
                            <ChevronUp size={18} />
                            Hide Metrics
                        </>
                    ) : (
                        <>
                            <ChevronDown size={18} />
                            View Metrics (For the Nerds)
                        </>
                    )}
                </button>
            </div>

            {showMetrics && (
                <div className="mt-5 rounded-xl border border-gray-200 bg-gray-50 p-5">
                    <div className="grid gap-4 sm:grid-cols-2">
                        {Object.entries(metrics).filter(([_, value]) => value !== null && value !== undefined).map(([key, value]) => (
                            <div key={key}>
                                <p className="text-sm text-gray-500">{metricLabels[key] ?? key}</p>
                                <p className="mt-1 font-medium text-gray-900">{formatMetric(key, value)}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </section>
    );
}

export default SummaryCard;
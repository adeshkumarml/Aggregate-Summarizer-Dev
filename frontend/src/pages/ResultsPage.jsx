import Navbar from "../components/Navbar"
import ResultsHeader from "../components/ResultsHeader";
import OverviewCard from "../components/OverviewCard";
import SummaryCard from "../components/SummaryCard";
import DownloadSection from "../components/DownloadSection";
import Footer from "../components/Footer"

import { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";

import { getResults, downloadResults } from "../services/api";

function ResultsPage(){
    const MODEL_LABELS = {
        "gpt-4o-mini": "GPT-4o-Mini",
        "gemini-3.1-flash-lite": "Gemini-3.1-Flash-Lite",
        "deepseek-v4-flash": "Deepseek-v4-Flash",
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": "Llama-3.3-70B-Instruct",
        "Qwen/Qwen3.5-9B": "Qwen3.5-9B",
        "MiniMaxAI/MiniMax-M3": "MiniMax M3"
    };

    const { jobId } = useParams();
    const location = useLocation();
    const { selectedModels=[], summaryStyle="" } = location.state || {}; 
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    useEffect(() => {
        async function fetchResults() {
            try {
                const response = await getResults(jobId);
                setResults(response);
            }
            catch (err) {
                setError(err.message);
            }
            finally {
                setLoading(false);
            }
        }
        fetchResults();
    }, [jobId]);

     async function handleDownload(format) {
        try {
            const blob = await downloadResults(jobId, format);
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = `summary.${format}`;
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        }
        catch (err) {
            alert(err.message);
        }
    }
    if (loading) {
        return (
            <>
                <Navbar />
                <main className="flex min-h-screen items-center justify-center bg-blue-50/30">
                    <p className="text-gray-600">Loading results...</p>
                </main>
                <Footer />
            </>
        );

    }

    if (error) {
        return (
            <>
                <Navbar />
                <main className="flex min-h-screen items-center justify-center bg-blue-50/30">
                    <p className="text-red-600">{error}</p>
                </main>
                <Footer />
            </>
        );
    }

    return (
        <>
            <Navbar />
            <main className="min-h-screen bg-blue-50/30">
                <div className="mx-auto max-w-6xl px-4 py-10 md:px-8 md:py-16">
                    <ResultsHeader />
                    <OverviewCard  selectedModels={selectedModels} summaryStyle={summaryStyle} />
                    
                    <SummaryCard title="Consolidated Summary" subtitle="Combined from all selected AI models." summary={results.consolidated_summary} isConsolidated={true}
                        metrics={{ agreement_score: results.agreement_score }} />
                    <h3 className="mt-12 text-center text-xl font-semibold text-gray-600 md:text-2xl">Supporting Summaries</h3>
                    
                    {
                        Object.entries(results.summaries).map(
                            ([modelName, summary]) => (
                                <SummaryCard key ={modelName} title={MODEL_LABELS[modelName] ?? modelName} subtitle="" summary={summary} metrics={results.scores[modelName]} />
                        ))}
                    <DownloadSection onDownloadPDF={()=>handleDownload("pdf")} onDownloadDOCX={()=>handleDownload("docx")} />

                </div>
            </main>
            <Footer />
        </>
    );
}

export default ResultsPage
import Navbar from "../components/Navbar";
import ProgressBar from "../components/ProgressBar";
import FileInfo from "../components/FileInfo";
import Footer from "../components/Footer";

import { useState, useEffect } from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom";

import { getJobStatus } from "../services/api";

function ProcessingPage(){
    const navigate = useNavigate();
    const { jobId } = useParams();
    const location = useLocation();
    const [progress, setProgress] = useState(0);
    const [statusLabel, setStatusLabel] = useState("Preparing document...");
    const fileName = location.state?.fileName || "Document";
    const fileSize = location.state?.fileSize ? `${(location.state.fileSize / (1024 * 1024)).toFixed(2)} MB`: "--";
    useEffect(() => { 
        let cancelled = false; 
        let timeoutId;
        async function pollStatus() {
            if (cancelled) return;

            try {
                const response = await getJobStatus(jobId);
                if (cancelled) return;
                setProgress(response.progress);
                switch (response.status) {
                    case "queued":
                        setStatusLabel("Waiting in queue...");
                        break;

                    case "processing":
                        if (response.progress <= 15)
                            setStatusLabel("Extracting text...");
                        else if (response.progress <= 30)
                            setStatusLabel("Preparing document...");
                        else if (response.progress <= 60)
                            setStatusLabel("Generating AI summaries...");
                        else if (response.progress <= 80)
                            setStatusLabel("Evaluating summaries...");
                        else if (response.progress <= 90)
                            setStatusLabel("Building final summary...");
                        else
                            setStatusLabel("Finishing up...");
                        break;

                    case "completed":
                        setProgress(100);
                        navigate(`/results/${jobId}`, {state: location.state,});
                        return;

                    case "failed":
                        alert("Document processing failed.");
                        return;

                    default:
                        setStatusLabel("Processing...");
                }   
            }

            catch (error) {
                console.error("Polling failed:", error);
                // Ignore transient failures and retry
            }

            timeoutId = setTimeout(pollStatus, 1000);
        }
        pollStatus();

        return () => { 
            cancelled = true; 
            clearTimeout(timeoutId); 
        } ;
    }, [jobId, navigate, location.state]);

    return (
        <>
            <Navbar />
            <main className="min-h-screen bg-blue-50/30">
            <div className="mx-auto flex max-w-3xl flex-col items-center px-4 py-20">
                
                <section className="w-full rounded-2xl bg-white p-8 md:p-12">
                    
                    <div className="text-center">
                        <h1 className="text-3xl font-bold text-gray-900 md:text-4xl">Processing Document</h1>
                            <p className="mt-4 text-gray-600">Your document is being summarized. This may take a few moments depending on 
                                the document size and selected AI models.
                            </p>
                    </div>
                    
                    <div className="mt-12">
                        <ProgressBar progress={progress} label={statusLabel} /> 
                    </div>

                    <div className="mt-12">
                        <FileInfo fileName={fileName} fileSize={fileSize} />
                    </div>

                    <div className="mt-10 text-center">
                        <p className="text-sm text-gray-500">Please don't close this tab while processing.</p>
                    </div>
                </section>
            </div>
            </main>
            <Footer />
        </>
    )
}

export default ProcessingPage;
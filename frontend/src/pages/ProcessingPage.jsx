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
        let intervalId;
        async function pollStatus() {
            try {
                const response = await getJobStatus(jobId);
                setProgress(response.progress);
                switch (response.status) {
                    case "queued":
                        setStatusLabel("Waiting in queue...");
                        break;
                    case "processing":
                        setStatusLabel("Generating summaries...");
                        break;
                    case "completed":
                        setProgress(100);
                        clearInterval(intervalId);
                        navigate(`/results/${jobId}`, {state: location.state});
                        break;
                    case "failed":
                        clearInterval(intervalId);
                        alert("Document processing failed.");
                        break;
                    default:
                        setStatusLabel("Processing...");

                }

            }
            catch (error) {
                console.error(error);
                clearInterval(intervalId);
            }
        }

        pollStatus();
        intervalId = setInterval(pollStatus, 1000);
        return () => clearInterval(intervalId);
    }, [jobId, navigate]);

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
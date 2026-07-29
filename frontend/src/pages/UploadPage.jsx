import Navbar from "../components/Navbar";
import FileUpload from "../components/FileUpload";
import ModelSelector from "../components/ModelSelector";
import StyleSelector from "../components/StyleSelector";
import GenerateButton from "../components/GenerateButton";
import HowToUse from "../components/HowToUse";
import Footer from "../components/Footer";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadDocument } from "../services/api";

function UploadPage(){

    const navigate = useNavigate();
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadError, setUploadError] = useState("");
    const [selectedModels, setSelectedModels] = useState([]);
    const [summaryStyle, setSummaryStyle] = useState("concise");
    const [isUploading, setIsUploading] = useState(false);
    const [apiError, setApiError] = useState("");
    const canGenerate = selectedFile !== null && selectedModels.length >= 1 && selectedModels.length <= 3;
    
    const handleGenerate = async () => {
        if (!selectedFile) {
            setUploadError("Please upload a document.");
            return;
        }
        if (selectedModels.length === 0) {
            setApiError("Please select at least one model.");
            return;
        }
        setApiError("");

        try {
            setIsUploading(true);
            const response = await uploadDocument(selectedFile, selectedModels, summaryStyle);
            navigate(`/processing/${response.job_id}`, {
                state: {fileName: selectedFile.name, fileSize: selectedFile.size, selectedModels, summaryStyle}
            });
        }
        catch (error) {
            console.error(error);
            setApiError("Failed to upload document. Please try again.");
        }
        finally {
            setIsUploading(false);
        }
    };

    return (
      <>
        <Navbar />
        <main className="min-h-screen bg-blue-50/30">
        <div className="mx-auto max-w-5xl px-6 py-10 sm:py-14">
            <h1 className="mb-4 text-center text-3xl font-bold sm:text-4xl md:text-5xl">
                Aggregate Document Summarizer
            </h1>
            <p className="mx-auto mb-12 max-w-2xl text-center text-base text-gray-600 sm:text-lg">
                Compare AI-generated summaries from multiple leading LLMs.
            </p>

        <FileUpload selectedFile={selectedFile} setSelectedFile={setSelectedFile} uploadError={uploadError} setUploadError={setUploadError} />
        <ModelSelector selectedModels={selectedModels} setSelectedModels={setSelectedModels} />
        <StyleSelector summaryStyle={summaryStyle} setSummaryStyle={setSummaryStyle}/>

        {apiError && ( <p className="mt-4 text-center text-red-600">{apiError}</p> )}

        <GenerateButton canGenerate={canGenerate} isUploading={isUploading} onGenerate={handleGenerate} />
        <HowToUse />
        </div>
        </main>
        <Footer />
      </>
    );
}

export default UploadPage;
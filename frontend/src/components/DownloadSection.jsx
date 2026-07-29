import { FileText, FileDown } from "lucide-react";

function DownloadSection({ onDownloadPDF, onDownloadDOCX }){
    
    return (
        <section className="mt-12 rounded-2xl bg-white p-6 md:p-8">
            <h2 className="text-xl font-semibold text-gray-900 text-center">Download Results</h2>
            
            <div className="mt-8 flex flex-col gap-4 sm:flex-row">
                <button onClick={onDownloadPDF} className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-blue-600 px-6
                                                            py-3 text-white transition hover:bg-blue-700">
                <FileDown size={20} />Download PDF</button>

                <button onClick={onDownloadDOCX} className="flex flex-1 items-center justify-center gap-2 rounded-xl border border-gray-300
                                                            bg-white px-6 py-3 transition hover:bg-gray-100">
                <FileText size={20} />Download DOCX</button>
            </div>
        </section>
    );
}

export default DownloadSection;
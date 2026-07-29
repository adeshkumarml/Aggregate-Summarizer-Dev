import { FileText } from "lucide-react";

function ResultsHeader({/*({ fileName, fileSize }8*/} ){
    
    return (
        <section className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 md:text-4xl">Summaries Ready!</h1>
            <p className="mx-auto mt-4 max-w-2xl text-sm text-gray-600 md:text-base">Your document has been successfully summarized.</p>
            
            {/*<div className="mt-8 flex justify-center">
                <div className="flex w-full max-w-md items-center gap-4 rounded-xl border border-blue-200 bg-white p-5">
                    
                    <div className="rounded-lg bg-blue-100 p-3">
                        <FileText className="text-blue-600" size={24} />
                    </div>

                    <div className="min-w-0 flex-1">
                        <p className="truncate text-base font-semibold text-gray-900 md:text-lg">{fileName}</p>
                        <p className="mt-1 text-sm text-gray-500">{fileSize}</p>
                    </div>

                </div>
            </div>*/}

        </section>
    );
}

export default ResultsHeader;
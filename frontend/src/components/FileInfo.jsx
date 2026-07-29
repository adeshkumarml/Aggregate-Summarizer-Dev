import { FileText } from "lucide-react";

function FileInfo( {fileName, fileSize }) {

    return (
         <div className="w-full rounded-xl border border-gray-200 bg-gray-50 p-5">
            <div className="flex items-center gap-4">

                <div className="rounded-lg bg-blue-100 p-3">
                    <FileText className="text-blue-600" size={24} />
                </div>

                <div className="min-w-0 flex-1">
                    <p className="truncate text-base font-semibold text-gray-900 md:text-lg">{fileName}</p>
                    <p className="mt-1 text-sm text-gray-500">{fileSize}</p>
                </div>
            </div>
        </div>
    );
}

export default FileInfo;
import { useRef, useState } from "react";
import { FaCloudUploadAlt } from "react-icons/fa";
import { FaFileAlt } from "react-icons/fa";
import { FaTimes } from "react-icons/fa";

const SUPPORTED_TYPES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain",];
const MAX_SIZE = 10 * 1024 * 1024;

function FileUpload({ selectedFile, setSelectedFile, uploadError, setUploadError,}) {
    const inputRef = useRef(null);
    const [dragActive, setDragActive] = useState(false);
    const validateFile = (file) => {
        if (!SUPPORTED_TYPES.includes(file.type)) {
            setUploadError("Only PDF, DOCX and TXT files are supported.");
            return false;
        }
        if (file.size > MAX_SIZE) {
            setUploadError("Maximum allowed size is 10 MB.");
            return false;
        }
        setUploadError("");
        return true;
    };

    const handleFile = (file) => {
        if (!file) return;
        if (!validateFile(file))
            return;
        setSelectedFile(file);
    };

    const handleBrowse = (event) => {
        handleFile(event.target.files[0]);
    };

    const handleDrop = (event) => {
        event.preventDefault();
        setDragActive(false);
        handleFile(event.dataTransfer.files[0]);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
        setDragActive(true);
    };

    const handleDragLeave = () => {
        setDragActive(false);
    };

    const removeFile = () => {
        setSelectedFile(null);
        setUploadError("");
        if (inputRef.current)
            inputRef.current.value = "";
    };

    return (
        <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={`rounded-2xl border-2 border-dashed p-8 text-center transition overflow-hidden ${dragActive ? "border-blue-600 bg-blue-50" : "border-gray-300 bg-white"}`}
        >
            <input ref={inputRef} type="file" hidden accept=".pdf,.doc,.docx,.txt" onChange={handleBrowse} />
            {
                !selectedFile ? (
                    <>
                        <FaCloudUploadAlt className="mx-auto mb-6 text-6xl text-blue-500" />
                        <h2 className="text-2xl font-semibold">Drop your document here</h2>
                        <p className="mt-2 text-gray-500">or</p>
                        <button onClick={() => inputRef.current.click()} className="mt-6 rounded-lg bg-blue-500 px-8 py-3 text-white transition hover:bg-blue-800">
                            Upload File
                        </button>
                    </>
                ) : (
                    
                    <>
                        <FaFileAlt className="mx-auto mb-4 text-5xl text-blue-600"/>
                        <h2 className="break-words text-xl font-semibold">{selectedFile.name}</h2>
                        <p className="mt-2 text-gray-500">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                        <p className="mt-3 font-medium text-green-600">✓ Ready to summarize</p>
                        <div className="mt-6 flex justify-center gap-4">
                            <button onClick={() => inputRef.current.click()} className="rounded-lg bg-blue-500 px-6 py-2 text-white hover:bg-blue-800">
                                Replace File
                            </button>
                            <button onClick={removeFile} className="rounded-lg border border-red-400 px-4 py-2 text-red-600 hover:bg-red-100">
                                <FaTimes />
                            </button>
                        </div>
                    </>
                )
            }

            <p className="mt-8 text-sm text-gray-500 py-1">Supports PDF, DOCX, and TXT</p>
            <p className="text-sm text-gray-500 py-2">Maximum size: 10 MB</p>
            <p className="text-sm text-gray-500 py-3"><i>No data is stored after processing.</i></p>
            {
                uploadError && (
                    <p className="mt-4 font-medium text-red-600">{uploadError}</p>
                )
            }
        </div>
    );
}

export default FileUpload;

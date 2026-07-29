function GenerateButton({ canGenerate, isUploading, onGenerate  }) {

    return (
        <section className="mt-8">
            <button 
                onClick={onGenerate}
                disabled={!canGenerate || isUploading}
                className={`w-full rounded-xl py-4 text-lg font-semibold transition-all duration-200
                    ${canGenerate && !isUploading? "bg-blue-500 text-white hover:bg-blue-800 hover:shadow-lg" : "cursor-not-allowed bg-gray-300 text-gray-500"}`}
            >
                {isUploading
                    ? "Uploading..."
                    : "Summarize"}
            </button>
        </section>
    );
}

export default GenerateButton;
function ProgressBar({ progress, label = "Summarizing..." }){

    return (
        <div className="w-full">
            
            <div className="mb-3 flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">{label}</span>
                <span className="text-sm font-semibold text-blue-600">{progress}%</span>
            </div>

             <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                <div className="h-full rounded-full bg-blue-600 transition-all duration-500 ease-in-out" style={{ width: `${progress}%` }}/>
            </div>
        </div>
    );
}

export default ProgressBar;
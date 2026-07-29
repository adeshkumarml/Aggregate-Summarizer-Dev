function OverviewCard({ selectedModels, summaryStyle }){

    return (
        <section className="mt-10 rounded-2xl bg-white p-6 md:p-8">
            <h2 className="text-2xl font-semibold text-gray-900 text-center">Summary Overview</h2>
            
            <div className="mt-6 grid gap-8 md:grid-cols-2">
                <div>
                    <h3 className="font-medium text-gray-800 text-center">Models Used</h3>
                    
                    <div className="mt-3 flex flex-wrap gap-2 justify-center">{selectedModels.map((model) => (
                            <span key={model} className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">{model}</span>
                        ))}
                    </div>
                </div>

                <div>
                    <h3 className="font-medium text-gray-800 text-center">Summary Style</h3>

                    <div className="mt-3 flex flex-wrap gap-2 justify-center">    
                        <span className="inline-flex rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">{summaryStyle}</span>
                    </div>

                </div>
            
            </div>
        </section>
    );
}

export default OverviewCard;
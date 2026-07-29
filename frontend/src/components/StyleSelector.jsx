const STYLES = [
    {
        id: "concise",
        title: "Concise",
        description: "Short, quick overview"
    },
    {
        id: "comprehensive",
        title: "Comprehensive",
        description: "Balanced detail"
    },
    {
        id: "detailed",
        title: "Detailed",
        description: "Maximum information"
    }
];

function StyleSelector({ summaryStyle, setSummaryStyle }) {

    return (
        <section className="mt-8 rounded-2xl bg-white p-8">
            <h2 className="mb-2 text-center text-2xl font-semibold">
                Summary Style
            </h2>

            <p className="mb-6 text-center text-gray-500">
                Choose how detailed the summary should be.
            </p>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 sm:gap-6">
                {STYLES.map((style) => {
                    const isSelected = summaryStyle === style.id;

                    return (
                        <div
                            key={style.id} onClick={() => setSummaryStyle(style.id)}
                            className={`relative cursor-pointer rounded-xl border p-4 transition
                                ${isSelected ? "border-blue-600 bg-blue-50" : "border-gray-200 bg-white hover:border-blue-500 hover:shadow-md"}`}
                        >
                            <input type="radio" checked={isSelected} readOnly className="absolute left-4 top-4 h-5 w-5 accent-blue-600"/>
                            <h3 className="mb-2 text-center text-lg font-semibold">
                                {style.title}
                            </h3>

                            <p className="text-center text-sm text-gray-500">
                                {style.description}
                            </p>
                        </div>
                    );
                })}
            </div>
        </section>
    );
}

export default StyleSelector;
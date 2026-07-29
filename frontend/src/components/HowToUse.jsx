const STEPS = [
    {
        number: "01",
        title: "Upload Document",
        description: "Upload or drag-and-drop a .pdf, .docx or .txt document from your device."
    },
    {
        number: "02",
        title: "Choose AI Models",
        description: "Select up to three AI models and choose your preferred summary style."
    },
    {
        number: "03",
        title: "Compare Results",
        description: "Receive each model's summary, evaluation metrics and one consolidated summary. That's it!"
    }
];

function HowToUse() {
    return (
        <section id="how-to-use" className="mt-20 pt-10">
            <h2 className="mb-10 text-center text-3xl font-bold">How It Works?</h2>
            <div className="grid gap-8 md:grid-cols-3">
                {STEPS.map((step) => (
                    <div key={step.number} className="rounded-2xl bg-white p-8 border-1 border-blue-400">
                        <div className="mb-5 text-4xl font-bold text-blue-600 text-center">{step.number}</div>
                        <h3 className="mb-3 text-xl font-semibold text-center">{step.title}</h3>
                        <p className="text-gray-600 text-center">{step.description}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default HowToUse;
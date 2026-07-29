import openailogo from "../assets/openailogo.png";
import geminilogo from "../assets/geminilogo.png";
import llamalogo from "../assets/llamalogo.png";
import deepseeklogo from "../assets/deepseeklogo.png";
import qwenlogo from "../assets/qwenlogo.png";
import minimaxlogo from "../assets/minimaxlogo.png";

const MODELS = [
    {
        id: "gpt-4o-mini",
        name: "GPT-4o-Mini",
        logo: openailogo,
    },
    {
        id: "gemini-3.1-flash-lite",
        name: "Gemini-3.1-Flash-Lite",
        logo: geminilogo,
    },
    {
        id: "deepseek-v4-flash",
        name: "DeepSeek-v4-Flash",
        logo: deepseeklogo,
    },
    {
        id: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        name: "Llama-3.3-70B-Instruct",
        logo: llamalogo,
    },
    {
        id: "Qwen/Qwen3.5-9B",
        name: "Qwen3.5-9B",
        logo: qwenlogo,
    },
    {
        id: "MiniMaxAI/MiniMax-M3",
        name: "MiniMax-M3",
        logo: minimaxlogo,
    },
];

function ModelSelector({ selectedModels, setSelectedModels }) {

    const toggleModel =(modelId) => {
        if (selectedModels.includes(modelId)) {
            setSelectedModels(
                selectedModels.filter((id) => id !== modelId)
            );
            return;
        }
        if (selectedModels.length >= 3) {
            return;
        }
        setSelectedModels([...selectedModels, modelId,]);
    };

    return (
        <section className="mt-10 rounded-2xl bg-white p-8">

            <h2 className="mb-2 text-2xl font-semibold text-center">
                Choose Models
            </h2>

            <p className="mb-6 text-gray-500 text-center">
                Select up to 3 models.
            </p>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 sm:gap-6">
                {MODELS.map((model) => {
                    const isSelected = selectedModels.includes(model.id);
                    const isDisabled = selectedModels.length >= 3 && !isSelected;
                    return (
                        <div
                            key={model.id} onClick={() => {if (!isDisabled) {toggleModel(model.id)}}}
                            className={`relative cursor-pointer rounded-xl border border-gray-200 bg-white p-4 sm:p-6 transition hover:border-blue-500 hover:shadow-md
                            ${ isSelected ? "border-blue-600 bg-blue-50" : "border-gray-200 bg-white hover:border-blue-500 hover:shadow-md"}
                            ${ isDisabled ? "cursor-not-allowed opacity-50" : ""}`}
                        >
                            <input type="checkbox" checked={isSelected} readOnly className="absolute left-4 top-4 h-5 w-5 accent-blue-600"/>
                            <img src={model.logo} alt={model.name} className="mx-auto mb-4 h-10 w-10 object-contain"/>

                            <h3 className="break-words text-center text-sm font-medium sm:text-base">
                                {model.name}
                            </h3>

                        </div>
                    );
                })}
            </div>
        </section>
    );
}

export default ModelSelector;
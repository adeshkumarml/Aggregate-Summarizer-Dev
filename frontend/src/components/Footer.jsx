function Footer() {

    return (
        <footer className="mt-24 border-t border-gray-200 bg-white">
            <div className="mx-auto max-w-7xl px-6 py-10 text-center">
                <h3 className="text-xl font-semibold text-blue-600">Aggregate Summarizer</h3>
                <p className="mt-2 text-gray-600">An AI-powered document summarization and benchmarking service.</p>
                <p className="mt-8 text-sm text-gray-500">© 2026 Aggregate Summarizer. All rights reserved.</p>

                <p className="mt-2 text-xs text-gray-400">
                    OpenAI, Google Gemini, DeepSeek, Meta Llama, Qwen and MiniMax names,
                    logos and trademarks are the property of their respective owners and
                    are used solely for identification purposes.
                </p>
            </div>
        </footer>
    );
}

export default Footer;
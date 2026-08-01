import { useNavigate, useLocation, Link } from "react-router-dom";
import logo from "../assets/logo.png"

function Navbar() {
    const navigate = useNavigate();
    const location = useLocation();
    const handleHowToUse = () => {
        if (location.pathname === "/") {
            document.getElementById("how-to-use")?.scrollIntoView({ behavior: "smooth" });
        } else {
            navigate("/", {
                state: {
                    scrollTo: "how-to-use",
                },
            });
        }
    }

    return (
        <nav className="border-b border-gray-200 bg-white">
            
            <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 px-8 pt-8 pb-5 md:flex-row md:gap-0 md:items-center md:py-5">
                <Link to="/" className="flex items-center gap-3">
                    <img src={logo} alt="Logo" className="h-6 w-4 md:h-10 md:w-8" />
                    <h1 className="text-xl font-bold text-blue-600 md:text-2xl">
                        AggregateSummarizer
                    </h1>
                </Link>
                <div className="flex flex-wrap justify-center gap-4 text-sm md:gap-8 md:text-base md:gap-0 text-gray-600">
                    <button onClick={handleHowToUse} className="hover:text-blue-600 transition">
                        How to Use
                    </button>
                    <a href="https://github.com/adeshkumarml/Aggregate-Summarizer-Dev" className="hover:text-blue-600 transition" target="_blank" rel="noopener noreferrer">
                        Documentation
                    </a>
                    <a href="mailto:adesh.ks2002@gmail.com?subject=Aggregate%20Summarizer%20Feedback" className="hover:text-blue-600 transition">
                        Feedback
                    </a>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
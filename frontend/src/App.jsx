import { Routes, Route } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import ProcessingPage from "./pages/ProcessingPage";
import ResultsPage from "./pages/ResultsPage";

function App(){
  return(
    <Routes>
      <Route path="/" element={<UploadPage />} />
      <Route path="/processing/:jobId" element={<ProcessingPage />} />
      <Route path="/results/:jobId" element={<ResultsPage />} />
    </Routes>
  )
}

export default App;
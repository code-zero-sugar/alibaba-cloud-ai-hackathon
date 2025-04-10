import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Investigator } from "./components/Investigator";
import { ReportingBot } from "./components/ReportingBot";

function App() {
  return (
    <Router>
      <div className="flex items-center justify-center h-screen bg-[url('/chatbot_background.jpg')] bg-cover bg-center">
        <Routes>
          <Route path="/investigator" element={<Investigator />} />
          <Route path="/reporting-bot" element={<ReportingBot />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

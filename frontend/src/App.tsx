import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "@/Home";
import Storage from "@/Storage";
import Settings from "@/Settings";
import Logging from "@/Logging";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/storage" element={<Storage />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/logs" element={<Logging />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

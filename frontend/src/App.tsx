import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "@/Home";
import Storage from "@/Storage";
import Settings from "@/Settings";
import Logs from "@/Logs";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/storage" element={<Storage />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/logs" element={<Logs />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "@/Home";
import Storage from "@/Storage";
import Settings from "@/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/storage" element={<Storage />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

import Home from "@/Home";
import Storage from "@/Storage";
import Settings from "@/Settings";
import Logging from "@/Logging";
import { Route, Routes } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/storage" element={<Storage />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/logging" element={<Logging />} />
    </Routes>
  );
}

export default App;

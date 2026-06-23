import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

import { useEffect, useState } from "react";

export function App() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main>
        <SidebarTrigger />
        <TimeDisplay />
      </main>
    </SidebarProvider>
  );
}

function TimeDisplay() {
  const [time, setTime] = useState<string>(new Date().toLocaleString());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2 className="text-2xl">Hora actual: {time}</h2>
    </div>
  );
}

export default App;

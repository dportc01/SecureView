import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";

import { useEffect, useState } from "react";
import { getCameras } from "./api/CameraClient";
import { CamerasContainer } from "./components/app-camerasContainer";

export function Home() {
  const [cameras_ids, setCameraIds] = useState<number[]>([]);

  useEffect(() => {
    getCameras().then(setCameraIds);
    // setCameraIds([0, 2, 4, 6]);
  }, []);

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader site="Home" />
        <main className="px-5">
          <TimeDisplay />
          <CamerasContainer ids={cameras_ids} />
        </main>
      </SidebarInset>
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
      <h2 className="text-base">Hora actual: {time}</h2>
    </div>
  );
}

export default Home;

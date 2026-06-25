import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";

import { useEffect, useState } from "react";
import { getCameras } from "./api/cameraClient";
import { CamerasContainer } from "./components/app-camerasContainer";
import { TimeDisplay } from "@/components/app-timedisplay";

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

export default Home;

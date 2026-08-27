import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";

import { useEffect, useState } from "react";
import { getCameras } from "./api/cameraClient";
import { CamerasContainer } from "@/components/home/home-camerasContainer";
import { TimeDisplay } from "@/components/home/home-timedisplay";
import { Toaster } from "@/components/ui/sonner";
import { Terminate } from "@/components/home/home-terminate";
import { Restart } from "@/components/home/home-restart";
import { Disclaimer } from "@/components/home/home-disclaimer";

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
          <div className="flex flex-col gap-6 py-6">
            <section>
              <CamerasContainer ids={cameras_ids} />
            </section>
            <section className="flex flex-col gap-6">
              <Restart />
              <Terminate />
              <Disclaimer />
            </section>
          </div>
        </main>
        <Toaster />
      </SidebarInset>
    </SidebarProvider>
  );
}

export default Home;

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";
import { CameraConfig } from "@/components/app-cameraConfig";
import { Button } from "./components/ui/button";
import { useState } from "react";

export function Settings() {
  const [unedited, setUnedited] = useState<boolean>(true);

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader site="Settings" />
        <main className="px-5 flex flex-col gap-10">
          <CameraConfig
            cameraId={0}
            unedited={unedited}
            setUnedited={setUnedited}
          />
          <Button className="max-w-md" disabled={unedited}>
            Save configuration
          </Button>
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}

export default Settings;

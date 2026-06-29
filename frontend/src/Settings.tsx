import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";
import { CameraConfig } from "@/components/app-cameraConfig";
import { Button } from "./components/ui/button";
import { useEffect, useState } from "react";
import { get_config } from "./api/settingsClient";
import { type ConfigJson } from "@/types/Conf";

export function Settings() {
  const [unedited, setUnedited] = useState<boolean>(true);
  const [conf, setConf] = useState<ConfigJson | null>(null);

  useEffect(() => {
    get_config().then(setConf);
  }, []);

  const CamerasConfigSet = conf ? (
    conf.cameras.map((camera) => (
      <CameraConfig
        key={camera.id}
        data={camera}
        unedited={unedited}
        setUnedited={setUnedited}
      />
    ))
  ) : (
    <span>
      No configuration data detected, make sure the backend is running
    </span>
  );

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader site="Settings" />
        <main className="px-5 flex flex-col gap-10">
          <span className="pt-3">
            If you have made changes and they don't appear here you might need
            to restart the backend
          </span>
          <section>{CamerasConfigSet}</section>
          <Button className="max-w-md" disabled={unedited}>
            Save configuration
          </Button>
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}

export default Settings;

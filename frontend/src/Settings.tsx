import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";
import { CameraConfig } from "@/components/app-cameraConfig";
import { Button } from "./components/ui/button";
import { useEffect, useState } from "react";
import { get_config, update_config } from "@/api/settingsClient";
import { type ConfigJson } from "@/types/Conf";
import { Toaster } from "@/components/ui/sonner";
import { toast } from "sonner";
import { restartSystem } from "@/api/systemClient";

export function Settings() {
  const [unedited, setUnedited] = useState<boolean>(true);
  const [conf, setConf] = useState<ConfigJson | null>(null);
  const [newConf, setNewConf] = useState<ConfigJson | null>(null);

  useEffect(() => {
    get_config().then((data) => {
      setConf(data);
      setNewConf(data);
    });
  }, []);

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
          <section className="flex gap-6 w-full">
            {!conf || !newConf ? (
              <span>
                No configuration data detected, make sure the backend is running
              </span>
            ) : (
              conf.cameras.map((camera) => (
                <CameraConfig
                  key={camera.id}
                  conf={camera}
                  setNewConf={setNewConf}
                  unedited={unedited}
                  setUnedited={setUnedited}
                />
              ))
            )}
          </section>
          <Button
            className="max-w-md"
            disabled={unedited}
            onClick={() => {
              if (newConf) {
                update_config(newConf);
                toast.promise(
                  (async () => {
                    const message = await restartSystem();

                    await new Promise((r) => setTimeout(r, 3000));

                    window.location.reload();

                    return message;
                  })(),
                  {
                    loading: "Restarting...",
                    success: (msg) => msg,
                    error: "No response, try reloading the page",
                    position: "top-center",
                  },
                );
              }
            }}
          >
            Save configuration
          </Button>
        </main>
        <Toaster />
      </SidebarInset>
    </SidebarProvider>
  );
}

export default Settings;

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";
import { CameraConfig } from "@/components/settings/app-cameraConfig";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { get_config, update_config } from "@/api/settingsClient";
import { type ConfigJson } from "@/types/Conf";
import { Toaster } from "@/components/ui/sonner";
import { toast } from "sonner";
import { restartSystem } from "@/api/systemClient";
import { AddCameraConf } from "@/components/settings/app-addCameraConf";
import { NotifTime } from "@/components/settings/app-notifTime";

export function Settings() {
  const [unedited, setUnedited] = useState<boolean>(true);
  const [conf, setConf] = useState<ConfigJson | null>(null);

  // const placeholder: ConfigJson = {
  //   notification_time: 90,
  //   cameras: [{ id: 0, start_record: "08:00", end_record: "22:00" }],
  // };

  useEffect(() => {
    get_config().then((data) => {
      setConf(data);
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
          <section className="flex flex-col gap-4">
            {!conf ? (
              <span>
                No configuration data detected, make sure the backend is running
              </span>
            ) : (
              <>
                <NotifTime
                  conf={conf}
                  setConf={setConf}
                  unedited={unedited}
                  setUnedited={setUnedited}
                />

                <div>
                  <AddCameraConf
                    conf={conf}
                    setConf={setConf}
                    unedited={unedited}
                    setUnedited={setUnedited}
                  />
                </div>

                <div className="grid grid-cols-3 gap-6 w-full">
                  {conf.cameras.map((camera) => (
                    <CameraConfig
                      key={camera.id}
                      conf={camera}
                      setConf={setConf}
                      unedited={unedited}
                      setUnedited={setUnedited}
                    />
                  ))}
                </div>
              </>
            )}
          </section>
          <section className="flex flex-col gap-1">
            <Button
              className="max-w-md"
              disabled={unedited}
              onClick={() => {
                if (conf) {
                  console.log(conf);
                  update_config(conf);
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
            <span className="text-muted-foreground">
              Saving the configuration will restart the backend
            </span>
          </section>
        </main>
        <Toaster />
      </SidebarInset>
    </SidebarProvider>
  );
}

export default Settings;

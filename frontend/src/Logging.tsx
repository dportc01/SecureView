import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Toaster } from "@/components/ui/sonner";
import { LogsText } from "@/components/logging/logging-text";
import { useEffect, useState } from "react";
import type { ResLogs } from "@/types/Logging";
import { clean_log, download_log, get_log } from "@/api/logClient";
import { Button } from "@/components/ui/button";
import { ArrowDownToLine, Trash2 } from "lucide-react";

export default function Logging() {
  const [log, setLog] = useState<ResLogs | null>(null);

  useEffect(() => {
    get_log().then(setLog);
  }, []);

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader site="Logging" />
        <main className="px-5">
          {log == null ? (
            <div className="pt-4">
              No logs found check that backend is running correctly and the file
              exists
            </div>
          ) : (
            <>
              <div className="flex flex-col pt-4 gap-2">
                <span>Last {log.logs.length} logs</span>
                <LogsText logs={log.logs} />
                Size: {log.size}
              </div>
              <div className="flex gap-6 py-4">
                <Button
                  variant={"secondary"}
                  className="text-log-error"
                  onClick={clean_log}
                >
                  Clean logs <Trash2 />
                </Button>
                <Button
                  variant={"secondary"}
                  className="text-log-info"
                  onClick={download_log}
                >
                  Full download <ArrowDownToLine />
                </Button>
              </div>
            </>
          )}
        </main>
        <Toaster />
      </SidebarInset>
    </SidebarProvider>
  );
}

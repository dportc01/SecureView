import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Toaster } from "@/components/ui/sonner";
import { LogsText } from "@/components/logs/logs-text";
import { useEffect, useState } from "react";
import type { Log } from "@/types/Log";
import { get_log } from "@/api/logClient";

export default function Logs() {
  const [logs, setLogs] = useState<Log[] | null>(null);

  useEffect(() => {
    get_log().then(setLogs);
  }, []);

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader site="Logs" />
        <main className="px-5">
          {logs == null ? (
            <div className="pt-4">
              No logs found check that backend is running correctly and the file
              exists
            </div>
          ) : (
            <div className="flex flex-col pt-4 gap-2">
              <span>Last {logs.length} logs</span>
              <LogsText logs={logs} />
            </div>
          )}
        </main>
        <Toaster />
      </SidebarInset>
    </SidebarProvider>
  );
}

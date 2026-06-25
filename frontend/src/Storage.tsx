import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";
import TableContainer from "./components/app-table/table-container";

export function Storage() {
  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader site="Storage" />
        <main className="px-5">
          <TableContainer />
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}

export default Storage;

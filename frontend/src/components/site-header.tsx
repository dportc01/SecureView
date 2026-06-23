import type { SiteName } from "@/sites";
import { SidebarTrigger } from "@/components/ui/sidebar";

export function SiteHeader({ site }: { site: SiteName }) {
  return (
    <header className="flex gap-4 py-2 px-4">
      <SidebarTrigger />
      <h1 className="text-xl">{site}</h1>
    </header>
  );
}

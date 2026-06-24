import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar";
import type { SiteName, SiteRoute } from "@/types/sites";
import { FilePlay, HouseIcon, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

type ContentType = {
  title: SiteName;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  route: SiteRoute;
};

const content: ContentType[] = [
  {
    title: "Home",
    icon: HouseIcon,
    route: "/",
  },
  {
    title: "Storage",
    icon: FilePlay,
    route: "/storage",
  },
  {
    title: "Settings",
    icon: Settings,
    route: "/settings",
  },
];

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { pathname } = useLocation();

  return (
    <Sidebar {...props}>
      <SidebarHeader className="flex flex-row items-center gap-2">
        <img
          src="/SecureView_logo.svg"
          alt="SecureView logo"
          className="h-5 w-auto"
        />
        <h1 className="text-xl font-medium">SecureView</h1>
      </SidebarHeader>
      <SidebarContent>
        {content.map((item) => {
          const Icon = item.icon;

          return (
            <Button
              key={item.title}
              asChild
              variant="ghost"
              className={`flex w-full justify-start gap-2 p-2 ${
                pathname === item.route ? "bg-muted" : ""
              }`}
            >
              <Link to={item.route}>
                <Icon className="w-4 h-4" />
                <span>{item.title}</span>
              </Link>
            </Button>
          );
        })}
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}

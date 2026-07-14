import { useTheme } from "./theme-provider";
import { Button } from "@/components/ui/button";
import { Moon, Sun } from "lucide-react";

export function ThemeIcon() {
  const { theme, setTheme } = useTheme();

  return theme === "dark" ? (
    <Button onClick={() => setTheme("light")} variant={"ghost"}>
      <Sun />
    </Button>
  ) : (
    <Button onClick={() => setTheme("dark")} variant={"ghost"}>
      <Moon />
    </Button>
  );
}

import { Label } from "@/components/ui/label";
import { Input } from "../ui/input";
import type { ConfigJson } from "@/types/Conf";
import { useState, type Dispatch, type SetStateAction } from "react";
import { Button } from "@/components/ui/button";
import { Pencil } from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

type Porps = {
  conf: ConfigJson;
  setConf: Dispatch<SetStateAction<ConfigJson | undefined>>;
  unedited: boolean;
  setUnedited: Dispatch<SetStateAction<boolean>>;
};

export function NotifTime({ conf, setConf, unedited, setUnedited }: Porps) {
  const [readOnly, setReadOnly] = useState<boolean>(true);
  const hours = Math.floor(conf.notification_time / 60);
  const minutes = conf.notification_time % 60;

  return (
    <div className="flex flex-row items-center gap-2">
      <span>Time between notifications: </span>
      <div className="flex flex-row gap-2">
        <Input
          id="notif-hours"
          type="number"
          min={0}
          max={24}
          step={1}
          readOnly={readOnly}
          value={hours}
          className={cn(
            "max-w-18",
            readOnly ? "text-muted-foreground" : "text-primary",
          )}
          onChange={(e) => {
            const value = Number(e.target.valueAsNumber);

            if (Number.isNaN(value)) return;

            let clamped = value;
            if (minutes <= 0) {
              if (value <= 0) {
                toast.warning("Value can not be bellow 0 hours, 1 minutes", {
                  position: "top-center",
                });
              }
              clamped = Math.min(24, Math.max(1, value));
            } else {
              clamped = Math.min(24, Math.max(0, value));
            }

            setConf((prev) => ({
              ...prev!,
              notification_time: clamped * 60 + minutes,
            }));
          }}
        />
        <Label htmlFor="notif-hours">Hours</Label>
      </div>
      <div className="flex flex-row gap-2">
        <Input
          id="notif-minutes"
          type="number"
          min={0}
          max={59}
          step={1}
          readOnly={readOnly}
          value={minutes}
          className={cn(
            "max-w-18",
            readOnly ? "text-muted-foreground" : "text-primary",
          )}
          onChange={(e) => {
            const value = Number(e.target.valueAsNumber);

            if (Number.isNaN(value)) return;

            let clamped = value;
            if (hours <= 0) {
              clamped = Math.min(59, Math.max(1, value));
            } else {
              clamped = Math.min(59, Math.max(0, value));
            }

            setConf((prev) => ({
              ...prev!,
              notification_time: hours * 60 + clamped,
            }));
          }}
        />
        <Label htmlFor="notif-minutes">Minutes</Label>
      </div>
      <Button
        variant={"ghost"}
        onClick={() => {
          setReadOnly(!readOnly);
          if (unedited) setUnedited(false);
        }}
      >
        <Pencil />
      </Button>
    </div>
  );
}

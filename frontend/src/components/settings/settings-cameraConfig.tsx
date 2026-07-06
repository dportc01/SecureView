import { Card } from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Minus, Pencil } from "lucide-react";
import { useState, type Dispatch, type SetStateAction } from "react";
import { cn } from "@/lib/utils";
import type { ConfigJsonCam, ConfigJson } from "@/types/Conf";
import { toast } from "sonner";

type Props = {
  conf: ConfigJsonCam;
  setConf: Dispatch<SetStateAction<ConfigJson | undefined>>;
  unedited: boolean;
  setUnedited: Dispatch<SetStateAction<boolean>>;
};

export function CameraConfig({ conf, setConf, unedited, setUnedited }: Props) {
  const [readOnlyStart, setReadOnlyStart] = useState<boolean>(true);
  const [readOnlyEnd, setReadOnlyEnd] = useState<boolean>(true);

  return (
    <Card className="p-4 max-w-md w-full">
      <FieldSet>
        <FieldLegend className="flex w-full items-center justify-between">
          Camera {conf.id} configuration
          <Button
            className="max-h-8 max-w-8"
            onClick={() => {
              toast.info(
                `Deleted config for camera ${conf.id}, save changes to apply`,
                {
                  position: "top-center",
                },
              );
              if (unedited) setUnedited(false);
              setConf((prev) => ({
                ...prev!,
                cameras: prev!.cameras.filter((cam) => cam.id !== conf.id),
              }));
            }}
          >
            <Minus />
          </Button>
        </FieldLegend>
        <FieldGroup className="pt-4">
          <Field>
            <FieldLabel htmlFor={`cam${conf.id}-start-time`}>
              Record start time
            </FieldLabel>
            <div className="flex items-center gap-2">
              <Input
                id={`cam${conf.id}-start-time`}
                type="time"
                defaultValue={conf.start_record}
                onChange={(e) =>
                  setConf((prev) => ({
                    ...prev!,
                    cameras: prev!.cameras.map((cam) =>
                      cam.id === conf.id
                        ? { ...cam, start_record: e.target.value }
                        : cam,
                    ),
                  }))
                }
                readOnly={readOnlyStart}
                className={cn(
                  readOnlyStart ? "text-muted-foreground" : "text-primary",
                )}
              />
              <Button
                variant={"ghost"}
                onClick={() => {
                  setReadOnlyStart(!readOnlyStart);
                  if (unedited) setUnedited(false);
                }}
              >
                <Pencil />
              </Button>
            </div>
            <FieldDescription>
              The time recording of the camera will start
            </FieldDescription>
          </Field>
          <Field>
            <FieldLabel htmlFor={`cam${conf.id}-end-time`}>
              Record end time
            </FieldLabel>
            <div className="flex items-center gap-2">
              <Input
                id={`cam${conf.id}-end-time`}
                type="time"
                defaultValue={conf.end_record}
                onChange={(e) =>
                  setConf((prev) => ({
                    ...prev!,
                    cameras: prev!.cameras.map((cam) =>
                      cam.id === conf.id
                        ? { ...cam, end_record: e.target.value }
                        : cam,
                    ),
                  }))
                }
                readOnly={readOnlyEnd}
                className={cn(
                  readOnlyEnd ? "text-muted-foreground" : "text-primary",
                )}
              />
              <Button
                variant={"ghost"}
                onClick={() => {
                  setReadOnlyEnd(!readOnlyEnd);
                  if (unedited) setUnedited(false);
                }}
              >
                <Pencil />
              </Button>
            </div>
            <FieldDescription>
              The time recording of the camera will end
            </FieldDescription>
          </Field>
        </FieldGroup>
      </FieldSet>
    </Card>
  );
}

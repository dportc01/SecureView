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
import { Pencil } from "lucide-react";
import { useState, type Dispatch, type SetStateAction } from "react";
import { cn } from "@/lib/utils";

type Props = {
  cameraId: number;
  unedited: boolean;
  setUnedited: Dispatch<SetStateAction<boolean>>;
};

export function CameraConfig({ cameraId, unedited, setUnedited }: Props) {
  const [readOnlyStart, setReadOnlyStart] = useState<boolean>(true);
  const [readOnlyEnd, setReadOnlyEnd] = useState<boolean>(true);

  return (
    <Card className="p-4 max-w-md">
      <FieldSet>
        <FieldLegend>Camera {cameraId} configuration</FieldLegend>
        <FieldGroup className="pt-4">
          <Field>
            <FieldLabel htmlFor={`cam${cameraId}-start-time`}>
              Record start time
            </FieldLabel>
            <div className="flex items-center gap-2">
              <Input
                id={`cam${cameraId}-start-time`}
                type="time"
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
            <FieldLabel htmlFor={`cam${cameraId}-end-time`}>
              Record end time
            </FieldLabel>
            <div className="flex items-center gap-2">
              <Input
                id={`cam${cameraId}-end-time`}
                type="time"
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

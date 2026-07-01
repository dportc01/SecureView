import { Plus } from "lucide-react";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import type { ConfigJson, ConfigJsonCam } from "@/types/Conf";
import { useState, type Dispatch, type SetStateAction } from "react";
import { toast } from "sonner";

type Porps = {
  conf: ConfigJson;
  setConf: Dispatch<SetStateAction<ConfigJson | null>>;
  unedited: boolean;
  setUnedited: Dispatch<SetStateAction<boolean>>;
};

export function AddCameraConf({ conf, setConf, unedited, setUnedited }: Porps) {
  const [newConf, setNewConf] = useState<ConfigJsonCam>({
    id: 0,
    start_record: "08:00",
    end_record: "22:00",
  });

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>
          Add new camera configuration <Plus />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>New camera configuration</DialogTitle>
          <DialogDescription>
            Add configurations to cameras based on ids. The id must be exaclty
            the same as the number of the target camera
          </DialogDescription>
        </DialogHeader>
        <FieldGroup>
          <Field>
            <FieldLabel htmlFor="new-id">Id</FieldLabel>
            <Input
              id="new-id"
              type="number"
              min={0}
              step={1}
              value={newConf.id}
              onChange={(e) => {
                const value = e.target.valueAsNumber;

                if (Number.isNaN(value)) return;

                setNewConf((prev) => ({
                  ...prev,
                  id: value,
                }));
              }}
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="new-start-time">Record start time</FieldLabel>
            <Input
              id="new-start-time"
              type="time"
              value={newConf.start_record}
              onChange={(e) =>
                setNewConf((prev) => ({
                  ...prev,
                  start_record: e.target.value,
                }))
              }
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="new-end-time">Record end time</FieldLabel>
            <Input
              id="new-end-time"
              type="time"
              value={newConf.end_record}
              onChange={(e) =>
                setNewConf((prev) => ({
                  ...prev,
                  end_record: e.target.value,
                }))
              }
            />
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose asChild>
            <Button>Cancel</Button>
          </DialogClose>
          <DialogClose asChild>
            <Button
              onClick={() => {
                if (conf.cameras.some((cam) => cam.id === newConf.id)) {
                  toast.error("Configuration for that camera already exists", {
                    position: "top-center",
                  });
                } else {
                  setConf((prev) => ({
                    ...prev!,
                    cameras: [...prev!.cameras, newConf],
                  }));
                  if (unedited) setUnedited(false);
                }
              }}
            >
              Confirm
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

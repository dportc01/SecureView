import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export function Disclaimer() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button style={{ maxWidth: "120px" }} variant={"outline"}>
          Legal Disclaimer
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Legal Disclaimer</DialogTitle>
        </DialogHeader>
        <p>
          The user is solely responsible for ensuring that the use of this
          software and any recorded footage complies with all applicable laws
          and regulations. Users are strongly advised to consult the privacy and
          data protection regulations applicable in their country or region
          before using the software.
        </p>
        <p>
          For users in the European Union, the General Data Protection
          Regulation (GDPR) and applicable national data protection laws may
          apply to the recording and processing of personal data.
        </p>
        <DialogFooter>
          <DialogClose asChild>
            <Button>Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

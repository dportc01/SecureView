import { Button } from "@/components/ui/button";
import { restartSystem } from "@/api/systemClient";
import { toast } from "sonner";

export function RestartSection() {
  return (
    <section className="flex flex-col gap-4">
      <h2 className="text-lg">Restart</h2>
      <p className="lg:w-[50vw]">
        System will restart and the page will be automatically reloaded.
        <br />
        Please only use this when you intend to make an update to the backend,
        like adding a new camera or updating the settings. Be mindfull of the
        scaling overhead due to the number of cameras, if the update doesn't
        seem to work reload after some seconds, if it still doesn't work, manual
        intervention is required.
      </p>
      <Button
        style={{ maxWidth: "120px" }}
        onClick={() => {
          toast.promise(
            (async () => {
              const message = await restartSystem();

              await new Promise((r) => setTimeout(r, 3000));

              window.location.reload();

              return message;
            })(),
            {
              loading: "Restarting...",
              success: (msg) => msg,
              error: "No response, try reloading the page",
              position: "top-center",
            },
          );
        }}
      >
        Restart
      </Button>
    </section>
  );
}

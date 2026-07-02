import { Button } from "@/components/ui/button";
import { terminateSystem } from "@/api/systemClient";

export function Terminate() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-lg">Terminate</h2>
      <p className="lg:w-[50vw]">
        This will not only terminate cameras but the entire backend process.
        <br />
        Please only use this when you intend to make the backend fully stop, be
        aware that stoping the backend requires to manualy start it again
      </p>
      <Button style={{ maxWidth: "120px" }} onClick={() => terminateSystem()}>
        Terminate
      </Button>
    </div>
  );
}

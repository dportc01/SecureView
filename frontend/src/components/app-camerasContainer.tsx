import { terminateCameras } from "@/api/cameraClient";
import { Camera } from "@/components/app-camera";
import { Button } from "@/components/ui/button";

export function CamerasContainer({ ids }: { ids: number[] }) {
  const cameras = ids.map((id) => {
    return <Camera key={id} id={id} />;
  });

  return (
    <div className="py-6 flex flex-col gap-6">
      <section className="flex flex-col gap-6">
        <h2 className="text-lg">List of cameras</h2>
        {cameras.length === 0 ? (
          <p>
            There were no cameras detected. Please check that the backend is
            running correctly or adjust the environment variables.
          </p>
        ) : (
          <div className="flex gap-10">{cameras}</div>
        )}
      </section>
      <section className="flex flex-col gap-6">
        <h2 className="text-lg">Terminate</h2>
        <p>
          This will not only terminate cameras but the entire backend process.
          <br />
          Please only use this when you intend to make an update to the backend,
          like adding a new camera or updating the settings.
        </p>
        <Button
          style={{ maxWidth: "120px" }}
          onClick={() => terminateCameras()}
        >
          Terminate
        </Button>
      </section>
    </div>
  );
}

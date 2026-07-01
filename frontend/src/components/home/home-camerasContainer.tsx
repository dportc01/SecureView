import { Camera } from "@/components/home/home-camera";

export function CamerasContainer({ ids }: { ids: number[] }) {
  const cameras = ids.map((id) => {
    return <Camera key={id} id={id} />;
  });

  return (
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
  );
}

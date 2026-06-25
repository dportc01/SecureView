import { checkStatus } from "./checkStatus";
import { type VideoFile } from "@/types/VideoFile";

const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  console.error("Missing env VITE_API_URL");
}

async function getFiles() {
  const res = await fetch(`${apiUrl}/storage/get`);

  await checkStatus(res);
  const data = await res.json();
  console.log(data);

  const files: VideoFile[] = data.map((file: VideoFile) => ({
    status: file.status,
    name: file.name,
    duration: file.duration,
    size: file.size,
  }));

  console.log(files);
  return files;
}

export { getFiles };

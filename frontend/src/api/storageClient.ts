import { checkStatus, readSucces } from "./resAnalyzer";
import { type VideoFile } from "@/types/VideoFile";

const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  console.error("Missing env VITE_API_URL");
}

async function getFilesInfo(): Promise<VideoFile[]> {
  const res = await fetch(`${apiUrl}/storage/get`);

  await checkStatus(res);
  const data = await res.json();

  const files: VideoFile[] = data.map((file: VideoFile) => ({
    status: file.status,
    name: file.name,
    duration: file.duration,
    size: file.size,
  }));

  return files;
}

async function downloadFile(name: string): Promise<void> {
  const res = await fetch(`${apiUrl}/storage/download`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      filename: name,
    }),
  });

  await checkStatus(res);

  const blob = await res.blob();

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = name + ".mp4";
  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(url);
}

async function deleteFiles(names: string[]): Promise<void> {
  const res = await fetch(`${apiUrl}/storage/delete`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      filenames: names,
    }),
  });

  await checkStatus(res);
  await readSucces(res);
}

export { getFilesInfo, downloadFile, deleteFiles };

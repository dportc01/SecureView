import { checkStatus } from "./resAnalyzer";

const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  console.error("Missing env VITE_API_URL");
}

async function getCameras(): Promise<number[]> {
  const res = await fetch(`${apiUrl}/cameras/discover`);
  console.log(res);

  await checkStatus(res);
  const data = await res.json();
  console.log(data);

  return data;
}

async function startCamera(id: number) {
  const res = await fetch(`${apiUrl}/cameras/${id}/start`, {
    method: "POST",
  });

  await checkStatus(res);
}

async function stopCamera(id: number) {
  const res = await fetch(`${apiUrl}/cameras/${id}/stop`, {
    method: "POST",
  });

  await checkStatus(res);
}

export { getCameras, startCamera, stopCamera };

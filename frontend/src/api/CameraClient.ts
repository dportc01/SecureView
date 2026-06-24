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

  checkStatus(res);
}

async function stopCamera(id: number) {
  const res = await fetch(`${apiUrl}/cameras/${id}/stop`, {
    method: "POST",
  });

  checkStatus(res);
}

async function terminateCameras() {
  const res = await fetch(`${apiUrl}/cameras/terminate`, {
    method: "POST",
  });

  checkStatus(res);
}

async function checkStatus(res: Response) {
  if (!res.ok) {
    let errorBody: unknown;

    try {
      errorBody = await res.json();
    } catch {
      errorBody = await res.text();
    }

    console.error("Cameras API error:", {
      status: res.status,
      body: errorBody,
    });

    throw new Error(`Request failed with status ${res.status}`);
  }
}
export { getCameras, startCamera, stopCamera, terminateCameras };

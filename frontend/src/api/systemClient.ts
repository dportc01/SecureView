import { checkStatus, readSucces } from "./resAnalyzer";

const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  console.error("Missing env VITE_API_URL");
}

async function terminateSystem(): Promise<void> {
  const res = await fetch(`${apiUrl}/system/terminate`, {
    method: "POST",
  });

  console.log(res);

  await checkStatus(res);
  await readSucces(res);
}

async function restartSystem(): Promise<string> {
  const res = await fetch(`${apiUrl}/system/restart`, {
    method: "POST",
  });

  await checkStatus(res);
  try {
    const body = await res.json();
    return typeof body === "string" ? body : "Operation successful";
  } catch {
    return "Operation successful";
  }
}

export { terminateSystem, restartSystem };

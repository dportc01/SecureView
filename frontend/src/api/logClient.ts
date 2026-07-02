import type { ResLogs, Log } from "@/types/Logging";
import { checkStatus, readSucces } from "./resAnalyzer";

const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  console.error("Missing env VITE_API_URL");
}

async function get_log(): Promise<ResLogs> {
  const res = await fetch(`${apiUrl}/log/get`);

  await checkStatus(res);
  const data = await res.json();
  const size = data.size;

  const logs: Log[] = data.logs.map((log: Log) => ({
    level: log.level,
    time: log.time,
    message: log.message,
    source: log.source,
  }));

  return { size: size, logs: logs };
}

async function clean_log(): Promise<void> {
  const res = await fetch(`${apiUrl}/log/clean`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
  });

  await checkStatus(res);
  await readSucces(res);
}

async function download_log(): Promise<void> {
  const res = await fetch(`${apiUrl}/log/download`);

  await checkStatus(res);

  const blob = await res.blob();

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "app.log";
  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(url);
}

export { get_log, clean_log, download_log };

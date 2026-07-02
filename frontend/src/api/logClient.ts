import type { Log } from "@/types/Log";
import { checkStatus } from "./resAnalyzer";

const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  console.error("Missing env VITE_API_URL");
}

async function get_log(): Promise<Log[]> {
  const res = await fetch(`${apiUrl}/log/get`);

  await checkStatus(res);
  const data = await res.json();

  const logs: Log[] = data.map((log: Log) => ({
    level: log.level,
    time: log.time,
    message: log.message,
    source: log.source,
  }));

  return logs;
}

export { get_log };

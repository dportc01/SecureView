import { type ConfigJson } from "@/types/Conf";
import { checkStatus, readSucces } from "./resAnalyzer";

const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  console.error("Missing env VITE_API_URL");
}

async function get_config(): Promise<ConfigJson> {
  const res = await fetch(`${apiUrl}/config/get`);

  await checkStatus(res);

  const body: ConfigJson = await res.json();
  console.log(body);

  if (!body.cameras || !body.notification_time)
    throw new Error("Invalid body response");

  return body;
}

async function update_config(newConfig: ConfigJson) {
  const res = await fetch(`${apiUrl}/config/update`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newConfig),
  });

  await checkStatus(res);
  await readSucces(res);
}

export { get_config, update_config };

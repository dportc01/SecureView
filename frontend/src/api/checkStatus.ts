export async function checkStatus(res: Response) {
  if (!res.ok) {
    let errorBody: unknown;

    try {
      errorBody = await res.json();
    } catch {
      errorBody = await res.text();
    }

    console.error("API error:", {
      status: res.status,
      body: errorBody,
    });

    throw new Error(`Request failed with status ${res.status}`);
  }
}

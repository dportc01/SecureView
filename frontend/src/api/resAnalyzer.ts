import { toast } from "sonner";

export async function checkStatus(res: Response) {
  if (!res.ok) {
    let errorBody;
    let message = "Something went wrong";

    try {
      errorBody = await res.json();

      if (errorBody.message) {
        message = errorBody.message;
      }
    } catch {
      errorBody = await res.text();
    }

    console.error("API error:", {
      status: res.status,
      body: errorBody,
    });
    toast.error(message, { position: "top-center" });

    throw new Error(`Request failed with status ${res.status}`);
  }
}

export async function readSucces(res: Response) {
  try {
    const body = await res.json();
    toast.success(body.message, { position: "top-center" });
  } catch {
    toast.success("Operation succes", { position: "top-center" });
  }
}

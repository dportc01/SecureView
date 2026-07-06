import { toast } from "sonner";

export async function resWrapper<T>(
  apiCall: () => Promise<T>,
): Promise<T | undefined> {
  try {
    return await apiCall();
  } catch (err) {
    if (err instanceof TypeError) {
      showError("Backend did not respond");
    } else if (err instanceof Error) {
      showError(err.message);
    } else {
      showError("Unexpected error");
    }

    // Propagate to upwards await
    throw err;
  }
}

export async function checkStatus(res: Response): Promise<void> {
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

      if (errorBody) {
        message = errorBody;
      }
    }

    console.error("API error:", {
      status: res.status,
      body: errorBody,
    });

    throw new Error(message);
  }
}

export async function readSucces(res: Response): Promise<void> {
  try {
    const body = await res.json();
    toast.success(body.message, { position: "top-center" });
  } catch {
    toast.success("Operation succes", { position: "top-center" });
  }
}

function showError(error: string) {
  toast.error(error, { position: "top-center" });
}

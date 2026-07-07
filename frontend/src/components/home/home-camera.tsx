import { useState } from "react";
import { startCamera, stopCamera } from "@/api/cameraClient";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardFooter,
  CardContent,
} from "@/components/ui/card";

const apiUrl = import.meta.env.VITE_API_URL;

export function Camera({ id }: { id: number }) {
  const [open, setOpen] = useState(false);

  return (
    <Card className="flex flex-col min-w-35">
      <CardHeader className="text-base">Camera {id}</CardHeader>
      <CardContent>
        {!open && (
          <img
            src={`${apiUrl}/cameras/${id}`}
            className="cursor-pointer"
            onClick={() => setOpen(true)}
            alt="No video stream found"
          />
        )}
        {open && (
          <div
            onClick={() => setOpen(false)}
            style={{
              position: "fixed",
              cursor: "pointer",
              top: 0,
              left: 0,
              width: "100vw",
              height: "100vh",
              background: "rgba(0,0,0,0.8)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              zIndex: 99,
            }}
          >
            <img
              src={`${apiUrl}/cameras/${id}`}
              className="
                h-[90vh] w-auto
                portrait:h-auto
                portrait:w-[90vw]
              "
            />
          </div>
        )}
      </CardContent>
      <CardFooter>
        <Button onClick={() => startCamera(id)}>Start</Button>
        <Button onClick={() => stopCamera(id)}>Stop</Button>
      </CardFooter>
    </Card>
  );
}

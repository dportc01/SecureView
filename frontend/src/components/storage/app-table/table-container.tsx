import type { VideoFile } from "@/types/VideoFile";
import { columns } from "./columns";
import { DataTable } from "./data-table";
import { getFilesInfo } from "@/api/storageClient";
import { useEffect, useState } from "react";

export default function TableContainer() {
  const [files, setFiles] = useState<VideoFile[]>([]);

  useEffect(() => {
    getFilesInfo().then(setFiles);
  }, []);

  function updateValues() {
    getFilesInfo().then(setFiles);
  }

  return (
    <div className="container mx-auto py-10">
      <DataTable columns={columns({ updateValues })} data={files} />
    </div>
  );
}

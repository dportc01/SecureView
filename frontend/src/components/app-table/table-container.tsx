import type { VideoFile } from "@/types/VideoFile";
import { columns } from "./columns";
import { DataTable } from "./data-table";
import { getFilesInfo } from "@/api/storageClient";
import { useEffect, useState } from "react";

// const data: VideoFile[] = [
//   {
//     status: "Finished",
//     name: "Vide_file_1",
//     duration: 34500,
//     size: "1132 MB",
//   },
//   {
//     status: "Recording",
//     name: "Vide_file_1",
//     duration: "N/A",
//     size: "1132 KB",
//   },
//   {
//     status: "Recording",
//     name: "Vide_file_1",
//     duration: "N/A",
//     size: "1132 KB",
//   },
//   {
//     status: "Finished",
//     name: "Vide_file_1",
//     duration: "N/A",
//     size: "1132 KB",
//   },
//   {
//     status: "Finished",
//     name: "Vide_file_1",
//     duration: "N/A",
//     size: "1132 KB",
//   },
// ];

export default function TableContainer() {
  const [files, setFiles] = useState<VideoFile[]>([]);

  useEffect(() => {
    getFilesInfo().then(setFiles);
  }, []);

  return (
    <div className="container mx-auto py-10">
      <DataTable columns={columns} data={files} />
    </div>
  );
}

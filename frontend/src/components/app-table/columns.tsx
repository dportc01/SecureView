"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { Check, Loader, Trash2, ArrowDownToLine } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { type VideoFile } from "@/types/VideoFile";
import { deleteFiles, downloadFile } from "@/api/storageClient";

export const columns = ({
  updateValues,
}: {
  updateValues: () => void;
}): ColumnDef<VideoFile>[] => [
  {
    id: "select",
    header: ({ table }) => {
      const hasSelection = table.getSelectedRowModel().rows.length > 0;
      const selectedFiles: string[] = table
        .getSelectedRowModel()
        .rows.map((row) => row.getValue("name"));

      return (
        <Button
          className="flex justify-center items-center w-30"
          variant={"destructive"}
          disabled={!hasSelection}
          onClick={() => {
            deleteFiles(selectedFiles).then(() => updateValues());
          }}
        >
          Delete Selecion
        </Button>
      );
    },
    cell: ({ row }) => {
      const status: VideoFile["status"] = row.getValue("status");

      return (
        status === "Finished" && (
          <div className="flex justify-center items-center w-30">
            <Checkbox
              checked={row.getIsSelected()}
              onCheckedChange={(value) => row.toggleSelected(!!value)}
              aria-label="Select row"
            />
          </div>
        )
      );
    },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status: VideoFile["status"] = row.getValue("status");
      return status === "Recording" ? (
        <div className="flex felx-row gap-4">
          <Loader size={20} /> {status}
        </div>
      ) : (
        <div className="flex felx-row gap-4">
          <Check size={20} /> {status}
        </div>
      );
    },
  },
  {
    accessorKey: "name",
    header: "File name",
  },
  {
    accessorKey: "duration",
    header: "Duration",
  },
  {
    accessorKey: "size",
    header: "Size",
  },
  {
    id: "download_action",
    size: 20,
    minSize: 20,
    maxSize: 20,
    cell: ({ row }) => {
      const filename: VideoFile["name"] = row.getValue("name");
      const status: VideoFile["status"] = row.getValue("status");

      return (
        <Button
          variant={"ghost"}
          disabled={status === "Recording"}
          onClick={() => downloadFile(filename)}
        >
          <ArrowDownToLine color="#86a7fc" />
        </Button>
      );
    },
  },
  {
    id: "delete_action",
    size: 20,
    minSize: 20,
    maxSize: 20,
    cell: ({ row }) => {
      const filename: VideoFile["name"] = row.getValue("name");
      const status: VideoFile["status"] = row.getValue("status");

      return (
        <Button
          variant={"ghost"}
          disabled={status === "Recording"}
          onClick={() => {
            deleteFiles([filename]).then(() => updateValues());
          }}
        >
          <Trash2 color="red" />
        </Button>
      );
    },
  },
];

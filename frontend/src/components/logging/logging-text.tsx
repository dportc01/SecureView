import type { Log } from "@/types/Logging";

export function LogsText({ logs }: { logs: Log[] }) {
  const formatted_logs = logs.map((log) => {
    let color;

    switch (log.level) {
      case "WARNING":
        color = "text-log-warning";
        break;

      case "ERROR":
        color = "text-log-error";
        break;

      case "INFO":
        color = "text-log-info";
        break;

      default:
        color = "text-primary";
    }

    return (
      <div
        key={`${log.time}-${log.source}-${log.message}`}
        className={`font-mono text-sm`}
      >
        {log.time} - {<span className={`${color}`}>{log.level}</span>} -{" "}
        {log.source} - {log.message}
      </div>
    );
  });

  return (
    <div
      className="bg-card rounded-md border p-4"
      style={{
        width: "80vw",
        height: "800px",
        overflowY: "scroll",
      }}
    >
      {formatted_logs}
    </div>
  );
}

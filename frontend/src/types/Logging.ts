export type ResLogs = {
  size: string;
  logs: Log[];
};

export type Log = {
  level: string;
  message: string;
  source: string;
  time: string;
};

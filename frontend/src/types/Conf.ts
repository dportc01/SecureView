export type ConfigJson = {
  notification_time: number;
  cameras: ConfigJsonCam[];
};

export type ConfigJsonCam = {
  id: number;
  start_record: string;
  end_record: string;
};

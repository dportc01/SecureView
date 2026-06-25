from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import subprocess
import json
from app.config import RECORD_DIR


class Status(str, Enum):
    RECORDING = "Recording"
    FINISHED = "Finished"


@dataclass
class VideoFile:
    name: str
    status: Status
    duration: float | None
    size: int


class StorageServive:
    def get_records(self) -> list[VideoFile]:
        video_files: list[VideoFile] = []

        folder = Path(RECORD_DIR)

        for file in folder.iterdir():
            if file.is_file():
                if ".tmp" in file.suffixes:
                    video_files.append(
                        VideoFile(
                            name=str(file),
                            status=Status.RECORDING,
                            duration=None,
                            size=file.stat().st_size,
                        )
                    )
                elif ".mp4" == file.suffix:
                    video_files.append(
                        VideoFile(
                            name=str(file),
                            status=Status.FINISHED,
                            duration=self._get_duration(file),
                            size=file.stat().st_size,
                        )
                    )

        return video_files

    def _get_duration(self, path: Path) -> float | None:
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    str(path),
                ],
                capture_output=True,
                text=True,
            )

            data = json.loads(result.stdout)
            return round(float(data["format"]["duration"]), 2)
        except Exception:
            return None

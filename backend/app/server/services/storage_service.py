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
    duration: str
    size: str


SIZE_BYTE = 1
SIZE_KB = 1024 * SIZE_BYTE
SIZE_MB = SIZE_KB * 1024
SIZE_GB = SIZE_MB * 1024
SIZE_TB = SIZE_GB * 1024


class StorageServive:
    def get_records(self) -> list[VideoFile]:
        video_files: list[VideoFile] = []

        folder = Path(RECORD_DIR)

        for file in folder.iterdir():
            if file.is_file():
                if ".tmp" in file.suffixes:
                    video_files.append(
                        VideoFile(
                            name=str(file.stem),
                            status=Status.RECORDING,
                            duration="N/A",
                            size=self._get_size_string(file.stat().st_size),
                        )
                    )
                elif ".mp4" == file.suffix:
                    video_files.append(
                        VideoFile(
                            name=str(file.stem),
                            status=Status.FINISHED,
                            duration=self._get_duration(file),
                            size=self._get_size_string(file.stat().st_size),
                        )
                    )

        return video_files

    def _get_duration(self, path: Path) -> str:
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
            duration = float(data["format"]["duration"])

            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)

            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except Exception:
            return "N/A"

    def _get_size_string(self, size: int) -> str:
        if size >= SIZE_TB:
            return f"{size / SIZE_TB:.2f} TB"
        elif size >= SIZE_GB:
            return f"{size / SIZE_GB:.2f} GB"
        elif size >= SIZE_MB:
            return f"{size / SIZE_MB:.2f} MB"
        elif size >= SIZE_KB:
            return f"{size / SIZE_KB:.2f} KB"
        else:
            return f"{size} Bytes"

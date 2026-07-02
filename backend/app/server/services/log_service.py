from pathlib import Path
from collections import deque
import logging
import re

LOG_PATTERN = re.compile(
    r"TIME:\s(?P<time>.*?)\s-\s"
    r"LEVEL:\s(?P<level>.*?)\s-\s"
    r"(?P<source>.*?)\s-\s"
    r"MESSAGE:\s(?P<message>.*)"
)

SIZE_BYTE = 1
SIZE_KB = 1024 * SIZE_BYTE
SIZE_MB = SIZE_KB * 1024
SIZE_GB = SIZE_MB * 1024
SIZE_TB = SIZE_GB * 1024


class LogService:
    def __init__(self) -> None:
        self.log_path = Path(__file__).resolve().parents[3] / "app.log"

        if not self.log_path.exists():
            raise FileNotFoundError(f"There is no file named {str(self.log_path)}")

    def read_log(self) -> list[dict] | None:

        try:
            with self.log_path.open("r", encoding="utf-8", errors="replace") as f:
                lines = deque(f, maxlen=100)

            return [
                parsed
                for line in lines
                if (parsed := self._parse_line(line))
            ]

        except Exception as e:
            logging.exception(e)
            return None

    def log_size(self) -> str:
        size = self.log_path.stat().st_size

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

    def clean_log(self) -> bool:
        try:
            with self.log_path.open("w", encoding="utf-8"):
                pass  # This truncates the file
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def _parse_line(self, line: str):
        match = LOG_PATTERN.match(line)
        if not match:
            return None
        return match.groupdict()

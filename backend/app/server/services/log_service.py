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


class LogService:
    def read_log(self) -> list[dict] | None:
        log_path = Path(__file__).resolve().parents[3] / "app.log"

        try:
            with log_path.open("r", encoding="utf-8", errors="replace") as f:
                lines = deque(f, maxlen=100)

            return [
                parsed
                for line in lines
                if (parsed := self._parse_line(line))
            ]

        except Exception as e:
            logging.exception(e)
            return None

    def _parse_line(self, line: str):
        match = LOG_PATTERN.match(line)
        if not match:
            return None
        return match.groupdict()

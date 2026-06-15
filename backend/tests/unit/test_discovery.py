import os
import pytest
from app.discovery import discover_cameras
from app.discovery import CameraType


def test_discover_cameras():
    if os.getenv("GITHUB_ACTIONS") == "true":
        pytest.skip("No cameras available in GitHub Actions")

    result = discover_cameras()
    assert len(result) == 1

    assert result == [{"id": 0, "type": CameraType.LOCAL}]

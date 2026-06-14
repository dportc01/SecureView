import os
import pytest
from app.discovery.discover_cameras import discover_camereas


def test_discover_cameras():
    if os.getenv("GITHUB_ACTIONS") == "true":
        pytest.skip("No cameras available in GitHub Actions")

    result = discover_camereas()
    assert len(result) >= 1

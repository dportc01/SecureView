import subprocess
import time
import requests


def start_server():
    return subprocess.Popen([
            "flask",
            "--app",
            "app.wsgi",
            "run",
            "--host",
            "127.0.0.1",
            "--port",
            "5001"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def wait_for_server(url, timeout=5):
    for _ in range(timeout * 10):
        try:
            r = requests.get(url)
            if r.status_code in (200, 404):
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.1)

    raise RuntimeError("Server never started")


def test_health_e2e():
    server = start_server()

    try:
        # wait until Flask is actually running
        wait_for_server("http://127.0.0.1:5001/health")

        # real HTTP call (true E2E)
        response = requests.get("http://127.0.0.1:5001/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    finally:
        # clean shutdown (important to avoid port leaks)
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()

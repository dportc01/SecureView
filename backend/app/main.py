from server import create_app
from workers import start_camera_workers

if __name__ == "__main__":

    app = create_app()
    app.run(host="0.0.0.0", port=5000)

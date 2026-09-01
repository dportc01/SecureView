# SecureView

SecureView is a program for small-scale surveillance. It implements video streaming and recording with image recognition, which it uses to send notifications through a Telegram bot.

This code was developed as the backbone for my Bachelor's Thesis in Ingeniería Informática at the Universidad de León, and serves as a collection of the competencies learned throughout the degree.

## Requirements

- Python 3
- Node.js 20+
- Make
- ffprobe

## Installation

1. Clone the repository.
2. Go inside `SecureView/`.
3. Install the dependencies by running:

   ```sh
   make install
   ```

4. Configure the environment variables.

   **`backend/.env`**
   - `TELEGRAM_BOT_TOKEN`: Token of the Telegram bot.
   - `TELEGRAM_ALLOWED_USERS`: IDs of the users that will receive notifications. If there are multiple users, separate them with commas (e.g., `user1,user2,user3`).
   - `FRONTEND_URLS`: URLs where the frontend is hosted to allow CORS. If there are multiple URLs, separate them with commas (e.g., `http://xxxx:5173,http://xxxx:80`).
   - `SERVER_PORT`: Port number of the Python backend server (default 5000).
   - `SERVER_THREADS`: Number of threads dedicated to handling parallel HTTP requests (default 8).
   - `MAX_LOCAL_CAMERA_INDEX`: Maximum number of local camera indexes to check, as assigned by the operating system. It is recommended to set this value higher than the expected number of connected cameras, as some operating systems may assign multiple indexes to different interfaces or aspects of the same physical camera (default 4).

   **`frontend/.env`** _(used for development)_
   - `VITE_API_URL`: URL of the Python backend server.

   **`frontend/.env.production`**
   - `VITE_API_URL`: URL of the Python backend server used in the production build.

5. Build the frontend by running:

   ```Shell
   make frontend-build
   ```

6. Expose the built files created on `frontend/dist/` trough your preffered method
7. Start the backend by running:

   ```Shell
   make backend
   ```

## Features and Usage

SecureView currently supports only cameras detected by OpenCV (`cv2`). To support additional camera sources, implement a class that inherits from `backend/app/camera/camera_interface.py` and update `backend/app/camera/factory.py` and `backend/app/discovery/discover_cameras.py` to instantiate and detect the new camera type.

Each camera records only if the current time is within its configured recording interval. If no recording interval is configured for a camera, it will not record. If the start and end times are identical, the camera records continuously.

Stopping, restarting, or terminating the backend will gracefully finish all recordings currently in progress.

Recordings are stored in `backend/video_records/`, while application logs are stored in `backend/app.log`.

Whenever an active camera detects a person, SecureView sends a Telegram notification with the camera ID and the captured frame. Each camera has its own notification cooldown, meaning that after Camera 0 sends a notification, Camera 2 can still immediately send one if it also detects a person.

Whenever cameras are connected or disconnected, the backend must be restarted so that it can detect the available devices.

Restarting the backend is also required after modifying the application settings.

The application consists of four pages:

### Home

The **Home** page displays all detected cameras. Cameras that are unavailable display a **"NO SIGNAL"** image. Cameras can be started or stopped using the **Start** and **Stop** buttons, and the video stream can be enlarged by clicking on it.

This page also includes the **Terminate** button, which completely stops the backend, and the **Restart** button, which restarts the application to apply configuration changes or detect the available cameras.

### Storage

The **Storage** page displays both ongoing and completed recordings, including information such as the recording name, duration, and file size. Completed recordings can be downloaded or deleted.

### Settings

The **Settings** page displays the current configuration. It allows the user to modify the notification cooldown and configure the recording intervals for individual cameras.

### Logging

The **Logging** page displays up to the last 100 lines of the application log, along with the total log file size. It also allows the user to download the complete log or delete its contents.

## Structure

### Backend structure

```
.
├── app/
│   ├── assets/							# Static resources
│   ├── camera/							# Camera interfaces and implementations
│   ├── config/							# Configuration loading and constants
│   ├── discovery/						# Camera discovery
│   ├── logging/						# Custom loggers
│   ├── messaging/						# Server to worker communication
│   ├── notification/					# Notification implementation
│   ├── object_recognition/				# Frame object recognition
│   ├── record/							# Video recording
│   ├── server/
│   │   ├── api/						# REST API endpoints
│   │   └── services/					# Business logic
│   ├── workers/						# Work loops and class orchestration
│   ├── __init__.py						# App package definition
│   └── main.py							# Entry point
└── tests/
    ├── integration/					# Integration tests
    └── unit/							# Unit tests
```

### Frontend structure

```
.
├── public								# Static resources
└── src									# Application source
    ├── api								# Api client
    ├── components						# React components
    │   ├── home						# Home page components
    │   ├── logging						# Logging page components
    │   ├── settings					# Settings page components
    │   ├── storage						# Storage page components
    │   └── ui							# Predefined shadcn/ui components
    ├── hooks							# Custom Hooks
    ├── lib								# Helper functions
    └── types							# Typescript types
```

## Development

Development utilities are already included in the project dependencies.

The `Makefile` also provides commands to help with development:

- `run` — Runs the frontend in development mode and the backend.
- `frontend` — Runs the frontend in development mode.
- `frontend-lint` — Lints the frontend using **ESLint**.
- `backend-test` — Runs Python tests using **pytest**.
- `backend-test-cov` — Runs tests and generates a coverage report.
- `backend-lint` — Lints the backend using **flake8**.
- `backend-clean` — Removes execution artifacts, and coverage caches.

### Testing

- Unit and integration tests included.
- Approximately **85% code coverage**.
- Coverage report available through `make backend-test-cov`.

## Contributing

Although contributions are welcome, this project is no longer under active development. If your changes are substantial, I recommend creating a fork and continuing development there in accordance with the project's license.

While not required, I would greatly appreciate a reference to the original repository if you build upon this project. :D

## Licensing

This project is licensed under the MIT License. See the `LICENSE` file for details.

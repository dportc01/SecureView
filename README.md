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
   - `SERVER_PORT`: Port number of the Python backend server.
   - `SERVER_THREADS`: Number of threads dedicated to handling parallel HTTP requests.

   **`frontend/.env`** _(used for development)_
   - `VITE_API_URL`: URL of the Python backend server.

   **`frontend/.env.prod`**
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

SecureView currently supports only cameras detected by OpenCV (`cv2`). However, it provides the necessary interface to implement additional camera sources in `backend/app/cameras/camera_interface.py`.

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
│   ├── assets/
│   ├── camera/
│   ├── config/
│   ├── discovery/
│   ├── logging/
│   ├── messaging/
│   ├── notification/
│   ├── object_recognition/
│   ├── record/
│   ├── server/
│   │   ├── api/
│   │   └── services/
│   └── workers/
└── tests/
    ├── integration/
    └── unit/
```

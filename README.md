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

6. Expose the built files created on `forntend/dist/` trough your preffered method
7. Start the backend by running:

   ```Shell
   make backend
   ```

## Usage

## Structure

### Backend structure

```
app
├── config/                      # Environment variables & global configuration
│   └── config.py
│
├── main.py                     # Development entry point
│
├── messaging/                  # Communication bus (Flask ↔ camera workers)
│   ├── bus_interface.py
│   ├── multiprocessing_bus.py
│   └── redis_bus.py
│
├── server/                     # Flask app initialization, routes, services
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── services/
│   │   └── camera_service.py
│   │
│   └── __init__.py
│
├── workers/                   # Camera worker system
│   ├── camera/
│   │   ├── camera_interface.py
│   │   └── usb_camera.py
│   │
│   ├── camera_worker.py        # Builds camera implementation
│   └── manager.py              # Orchestrates all camera workers
│
└── wsgi.py                    # Production Flask entry point
```

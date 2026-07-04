# SecureView

!!!! REQUIRES ffprobe

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

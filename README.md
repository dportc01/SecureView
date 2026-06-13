# SecureView

## Structure

### Backend structure

```
.
├── config ➜ Env variables and general configuration
│   └── config.py
├── main.py ➜ Dev entry point
├── messaging ➜ Communication bus between Flask server and camera workers
│   ├── bus_interface.py
│   ├── multiprocessing_bus.py
│   └── radis_bus.py
├── server ➜ Flask initialization, routes, coms...
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── __init__.py
│   └── services
│       └── camera_service.py
├── workers ➜ Camera workers initilization
│   ├── camera
│   │   ├── camera_interface.py
│   │   └── usb_camera.py
│   ├── camera_worker.py ➜ Builds camera implementation
│   └── manager.py ➜ Builds all camera workers
└── wsgi.py ➜ Flask server entry point
```

# SecureView

## Structure
### Backend structure
```
.
├── config
│   └── config.py
├── main.py
├── messaging
│   ├── bus_interface.py
│   ├── multiprocessing_bus.py
│   └── radis_bus.py
├── server
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── __init__.py
│   └── services
│       └── camera_service.py
├── workers
│   ├── camera
│   │   ├── camera_interface.py
│   │   └── usb_camera.py
│   ├── camera_worker.py
│   └── manager.py
└── wsgi.py
```

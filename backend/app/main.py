from flask import Flask, Response
from camera import Camera

app = Flask(__name__)

camera = Camera()

@app.route('/video')
def video():
    return Response(
        camera.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
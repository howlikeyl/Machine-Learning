from Movement import move, get_distance, move_camera
from flask import Flask, Response, render_template
from picamera2 import Picamera2
import cv2
import time
from picarx import Picarx

px = Picarx()
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}))
camera.start()
app = Flask(__name__)
last_frame = None
def capture_frame():
    global last_frame
    frame = camera.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # fix color
    _,jpeg = cv2.imencode('.jpg', frame)
    jpg_bytes = jpeg.tobytes()
    last_frame = jpg_bytes
    return last_frame

def video_stream():
    while True:
        frame = capture_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + 
                   frame + b'\r\n')
        time.sleep(.03)
@app.route('/move/<direction>')
def handle_movement(direction):
    if direction in ["forward", "backward", "left", "right", "stop", "backward_left", "backward_right"]:
        move(direction)
        return "Robot Moving"
    else:
        return "invalid"

@app.route('/video')
def video():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/index')
def index():
    return render_template('Controller.html')
@app.route('/camera/<direction>')
def handle_camera(direction):
    if direction in ["up", "down", "left", "right"]:
        move_camera(direction)
        return "camera moving"
    else:
        return "invalid"
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        px.stop()
        px.set_dir_servo_angle(0)
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)

          
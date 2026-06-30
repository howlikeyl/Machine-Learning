Name: Senghak Heng
# PiCar-X Autonomous Robot
A robot rover built on the SunFounder PiCar-X kit and a Raspberry Pi Zero 2 W, in Python. It runs two ways: fully autonomous obstacle avoidance, or remote web control from a browser with a live camera feed. Object detection is planned next.

## Hardware
SunFounder PiCar-X kit (chassis, motors, steering + camera servos, ultrasonic sensor, Robot HAT V4), Raspberry Pi Zero 2 W (512 MB RAM, `aarch64`), 32 GB microSD card, battery pack, and a camera module on the CSI port.

## Setup
Flash the SD card with Raspberry Pi Imager (Raspberry Pi OS), setting the hostname, username, password, Wi-Fi, and enabling SSH — a headless setup with no monitor needed. Then connect: `ssh sheng@picarx1.local`

## Install the libraries (SunFounder's "Install All the Modules")
1. `sudo apt update && sudo apt upgrade`
2. `cd ~ && git clone -b 2.5.x https://github.com/sunfounder/robot-hat.git --depth 1 && cd robot-hat && sudo python3 install.py`
3. `cd ~ && git clone https://github.com/sunfounder/vilib.git --depth 1 && cd vilib && sudo python3 install.py`
4. `cd ~ && git clone -b 2.1.x https://github.com/sunfounder/picar-x.git --depth 1 && cd picar-x && sudo pip3 install . --break-system-packages`
5. `cd ~/robot-hat && sudo bash i2samp.sh`

The stack is layered: your code → **picar-x** → **robot-hat** → GPIO.

Then calibrate the servos and motors: `cd ~/picar-x/example/calibration && sudo python3 calibration.py`

## Running

**Autonomous mode:**
```
sudo python3 Movement.py     # Ctrl+C to stop
```
Put the robot on the floor with clear space first — it drives on its own.

**Web control mode:**
```
sudo python3 app.py
```
Then open `http://picarx1.local:5000/index` in a browser on the same Wi-Fi (or use the Pi's IP from `hostname -I`).

## How `Movement.py` works (autonomous)
Key API: `forward(speed)` / `backward(speed)` (speed 0–100), `stop()`, `set_dir_servo_angle(angle)` (0 = straight, − = left, + = right), `set_cam_pan_angle` / `set_cam_tilt_angle`, `get_distance()` for the ultrasonic sensor.

- Obstacle avoidance (detect-turn-recheck): because the sensor is fixed forward, the robot can't scan sideways. So it drives forward while clear, and when blocked it turns a little and lets the next loop re-read the sensor. Against a long wall it keeps turning incrementally until the path opens, instead of getting stuck. (Needs more improvement if the obstacle is very long.)
- Safety: the loop is wrapped in `try`/`finally`, with `px.stop()` and servo resets in the `finally`. This runs on `Ctrl+C` or any crash, so the robot always stops cleanly instead of driving away.
- `move(direction)` handles `forward`, `backward`, `left`, `right`, `backward_left`, `backward_right`, `stop` — turning steers the wheels and drives at the same time.
- `move_camera(direction)` pans/tilts the camera in 5° steps, clamped to ±30° (the safe range SunFounder uses for these servos).

## How the web control works (`app.py` + `Controller.html`)
`app.py` is a Flask server that turns the Pi into a web-controlled robot. `Movement.py` knows how to drive the hardware; `app.py` exposes that over the web.

Routes:
- `/index` — serves the control page (live video + buttons)
- `/video` — live MJPEG camera stream
- `/move/<direction>` — drive the robot
- `/camera/<direction>` — pan/tilt the camera

The page (`templates/Controller.html`) has a drive pad and a camera pad. Driving is press-and-hold (release to stop); the camera holds-to-pan using a repeating timer. A **reverse toggle** remaps the drive pad: when on, left/right back up while steering (`backward_left` / `backward_right`) and the forward button is disabled.

The camera is captured with **picamera2** (not OpenCV's `VideoCapture`, which fails on the Pi Zero 2 W with a GStreamer memory error), then encoded to JPEG with OpenCV for streaming.

## Editing workflow
Edit on the Mac and copy over with `scp Movement.py sheng@picarx1.local:/home/sheng/` (HTML goes in `templates/`), or edit directly on the Pi with `nano`. VS Code Remote-SSH works too, but its server is heavy for the Pi Zero 2 W's 512 MB RAM and the connection can drop, so scp/nano is more reliable.

## Troubleshooting
- `lgpio.error: 'GPIO busy'` — a previous run still holds the pins. Run `sudo pkill -f Movement.py`, or `sudo reboot` if that fails.
- Camera `Failed to allocate required memory` (GStreamer) — OpenCV is using the wrong backend; capture with picamera2 instead (as `app.py` does).
- SSH timeout — the Pi is asleep, off Wi-Fi, or out of power; check the green LED, or connect by IP instead of `.local`.
- Runaway robot on exit — make sure the loop has `try`/`finally` with `px.stop()`.
- Wrong prompt — `...MacBook-Pro` is the Mac, `sheng@picarx1` is the Pi. Robot code lives on the Pi.

## Roadmap
1. Autonomous obstacle avoidance — working (`Movement.py`)
2. Manual web control + live video — working (`app.py` + `Controller.html`)
3. Combined manual + autonomous mode with a toggle (threading)
4. Object detection — YOLO + OpenCV with text-to-speech labels

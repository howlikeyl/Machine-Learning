# PiCar-X Autonomous Robot
An autonomous obstacle-avoidance rover built on the SunFounder PiCar-X kit and a Raspberry Pi Zero 2 W, in Python. It drives forward on its own, reads an ultrasonic sensor, and steers around obstacles. Web control and object detection are planned next.

## Hardware
SunFounder PiCar-X kit (chassis, motors, steering + camera servos, ultrasonic sensor, Robot HAT V4), Raspberry Pi Zero 2 W (512 MB RAM, `aarch64`), 32 GB microSD card, battery pack, and a camera module on the CSI port.

## Setup
Flash the SD card with Raspberry Pi Imager (Raspberry Pi OS), setting the hostname, username, password, Wi-Fi, and enabling SSH — a headless setup with no monitor needed. Then connect: ssh sheng@picarx1.local


## Install the libraries (SunFounder's "Install All the Modules"):
1. sudo apt update && sudo apt upgrade
2. cd ~ && git clone -b 2.5.x https://github.com/sunfounder/robot-hat.git --depth   1 && cd robot-hat && sudo python3 install.py
3. cd ~ && git clone https://github.com/sunfounder/vilib.git --depth 1 && cd vilib && sudo python3 install.py
4. cd ~ && git clone -b 2.1.x https://github.com/sunfounder/picar-x.git --depth 1 && cd picar-x && sudo pip3 install . --break-system-packages
5. cd ~/robot-hat && sudo bash i2samp.sh

- The stack is layered: your code → **picar-x** → **robot-hat** → GPIO.

- Then calibrate the servos and motors: cd ~/picar-x/example/calibration && sudo python3 calibration.py

## Running
sudo python3 Movement.py     # Ctrl+C to stop
Put the robot on the floor with clear space first — it drives on its own.

## How `Movement.py` works
Key API: `forward(speed)` / `backward(speed)` (speed 0–100), `stop()`, `set_dir_servo_angle(angle)` (0 = straight, − = left, + = right), `get_distance()` for the ultrasonic sensor.

- Obstacle avoidance (detect-turn-recheck): because the sensor is fixed forward, the robot can't scan sideways. So it drives forward while clear, and when blocked it turns a little and lets the next loop re-read the sensor. Against a long wall it keeps turning incrementally until the path opens, instead of getting stuck. (need more improvement if the obstacle is lengthy)

- Safety: the loop is wrapped in `try`/`finally`, with `px.stop()` and servo resets in the `finally`. This runs on `Ctrl+C` or any crash, so the robot always stops cleanly instead of driving away.

## Editing workflow
Edit on the Mac and copy over with `scp Movement.py sheng@picarx1.local:/home/sheng/`, or edit directly on the Pi with `nano Movement.py`. VS Code Remote-SSH works too, but its server is heavy for the Pi Zero 2 W's 512 MB RAM and the connection can drop, so scp/nano is more reliable.

## Troubleshooting

- `lgpio.error: 'GPIO busy'` — a previous run still holds the pins. Run `sudo pkill -f Movement.py`, or `sudo reboot` if that fails.
- SSH timeout — the Pi is asleep, off Wi-Fi, or out of power; check the green LED, or connect by IP instead of `.local`.
- Runaway robot on exit — make sure the loop has `try`/`finally` with `px.stop()`.
- Wrong prompt — `...MacBook-Pro` is the Mac, `sheng@picarx1` is the Pi. Robot code lives on the Pi.

## Roadmap
1. Autonomous obstacle avoidance — working (`Movement.py`)
2. Manual web control + live video — Flask (`app.py`); in progress
3. Combined manual + autonomous mode with a toggle (threading)
4. Object detection — YOLO + OpenCV with text-to-speech labels

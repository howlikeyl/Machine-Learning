# PiCar-X Autonomous Robot
A robot rover built on the SunFounder PiCar-X kit and a Raspberry Pi Zero 2 W, in Python. It runs three ways: fully autonomous obstacle avoidance, remote web control from a browser with a live camera feed, or a hands-free AI voice assistant. Object detection is planned next.

## Hardware
SunFounder PiCar-X kit (chassis, motors, steering + camera servos, ultrasonic sensor, Robot HAT V4), Raspberry Pi Zero 2 W (512 MB RAM, `aarch64`), 32 GB microSD card, battery pack, a camera module on the CSI port, and a USB microphone + speaker for the voice assistant.

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

For the voice assistant, also install:
```
pip3 install google-generativeai gTTS SpeechRecognition --break-system-packages
sudo apt install -y mpg123 python3-pyaudio flac
```

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

**Voice assistant mode:**
```
export GEMINI_API_KEY="your-key"   # or set it in ~/.bashrc
python3 LLM_test.py
```
Type `a` to ask by keyboard, `t` to speak, or `q` to quit. No `sudo` needed — it only uses the mic, speaker, and internet, not the GPIO.

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

## How the voice assistant works (`LLM_test.py`)
A hands-free AI assistant. You ask a question by typing or speaking, it sends the question to Google's Gemini model, prints the answer, and speaks it aloud through the robot's speaker.

The pipeline:
- **Speech-to-text** — `SpeechRecognition` records from the USB mic and transcribes speech to text via Google's free service (with `adjust_for_ambient_noise` to handle background noise).
- **LLM** — the text is sent to Gemini (`gemini-2.5-flash`) through the API, using a key read from the `GEMINI_API_KEY` environment variable (never hardcoded, so it stays out of the repo).
- **Text-to-speech** — the answer is cleaned of Markdown, converted to audio with `gTTS`, and played through the speaker (card 1) with `mpg123`.

Both typed and spoken input feed the same Gemini call, and the network/API calls are wrapped in `try/except` so a dropped connection prints a message instead of crashing.

Note: the LLM has a knowledge cutoff, so it can't answer questions about very recent events unless given live data.

## Editing workflow
Edit on the Mac and copy over with `scp Movement.py sheng@picarx1.local:/home/sheng/` (HTML goes in `templates/`), or edit directly on the Pi with `nano`. VS Code Remote-SSH works too, but its server is heavy for the Pi Zero 2 W's 512 MB RAM and the connection can drop, so scp/nano is more reliable.

## Troubleshooting
These are problems I actually ran into while building this, and how I fixed them.

### Movement.py (autonomous)
- **"GPIO busy" error** — this happened a lot. It means an old run of the program is still holding the pins. I fixed it with `sudo pkill -f Movement.py`, and if that didn't work, `sudo reboot` always cleared it.
- **The robot kept driving after I stopped the program** — pressing Ctrl+C killed the code but the motors kept going with the last command. I fixed this by wrapping the loop in `try`/`finally` and putting `px.stop()` in the `finally`, so it always stops no matter how the program ends.

### app.py (web control)
- **Camera "Failed to allocate required memory"** — OpenCV's `VideoCapture` just wouldn't work on the Pi Zero. I switched to picamera2 to grab the frames instead and that fixed it.
- **The robot still worked even after I thought I closed the program** — turns out the Flask server was still running in the background. Ctrl+C in the right terminal stops it, or `sudo pkill -f app.py`. I used `ps aux | grep app.py` to check if it was still alive.
- **The page wouldn't load on my phone** — I had to make sure my phone was on the same Wi-Fi, add `/index` to the end of the URL, and run Flask with `host='0.0.0.0'`. When `picarx1.local` didn't work I used the Pi's IP from `hostname -I` instead.

### LLM_test.py (voice assistant)
- **No sound from the speaker** — the speaker is on card 1, but the program was playing to the default (HDMI). Adding `-a plughw:1,0` to the mpg123 command fixed it. Also I had to make sure I actually installed the audio stuff (`i2samp.sh`) and reboot.
- **The Pi couldn't find the mic** — `arecord -l` showed nothing at first because I hadn't plugged it in. Once plugged in it showed up as its own card (card 2).
- **The robot said "star star Russia"** — Gemini writes answers in Markdown (`**bold**`), and the text-to-speech read the stars out loud. I stripped the `*` out of the answer before speaking it.
- **"UnknownValueError"** — this means it recorded but couldn't understand me. I had to speak clearly right after the prompt, and adding `adjust_for_ambient_noise` helped a lot.
- **401 / authentication error** — my API key wasn't set right. I checked with `[ -n "$GEMINI_API_KEY" ] && echo set`.
- **"ModuleNotFoundError" even though I installed it** — I installed the library as my normal user but ran the script with `sudo`, which looks in a different place. Fixed it by running without `sudo` (the voice assistant doesn't need it).

### General
- **SSH just times out** — usually the Pi was asleep, off Wi-Fi, or the battery died. I checked the green LED and power, or connected by IP instead of `.local`.
- **Editing the wrong file** — I kept mixing up my Mac and the Pi. The prompt tells you: `...MacBook-Pro` is my Mac, `sheng@picarx1` is the Pi. The robot code lives on the Pi, so I had to make sure I was editing there.

## Roadmap
1. Autonomous obstacle avoidance — working (`Movement.py`)
2. Manual web control + live video — working (`app.py` + `Controller.html`)
3. Hands-free AI voice assistant — working (`LLM_test.py`)
4. Combined manual + autonomous mode with a toggle (threading)
5. Object detection — YOLO + OpenCV with text-to-speech labels

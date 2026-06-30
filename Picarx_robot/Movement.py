from picarx import Picarx
import time
# create object of Picarx class
px = Picarx()

def get_distance():
    distance = px.get_distance()
    if distance is None or distance <= 0:
        return 30
    return distance

def move_forward(speed):
    px.set_dir_servo_angle(0)
    px.forward(speed)

def scan_obstacle():
    px.set_dir_servo_angle(0)

def scan_surrounding():
    px.set_cam_pan_angle(-35) # turn left
    time.sleep(0.5)
    left = get_distance()
    px.set_cam_pan_angle(35) # turn right
    time.sleep(.5)
    right = get_distance()
    px.set_cam_pan_angle(0) # turn center
    return left, right

cam_pan_angle = 0
cam_tilt_angle = 0
def move_camera(direction):
    global cam_pan_angle, cam_tilt_angle
    match direction:
        case "up":
            cam_tilt_angle += 5
        case "down":
            cam_tilt_angle -= 5
        case "left":
            cam_pan_angle -= 5
        case "right":
            cam_pan_angle += 5
    if cam_tilt_angle > 30: 
        cam_tilt_angle = 30
    elif cam_tilt_angle < -30: 
        cam_tilt_angle = -30
    if cam_pan_angle > 30:
        cam_pan_angle = 30
    elif cam_pan_angle < -30:
        cam_pan_angle = -30
    px.set_cam_pan_angle(cam_pan_angle)
    px.set_cam_tilt_angle(cam_tilt_angle)
        
def move(direction):
    match direction:
        case "forward": 
            px.set_dir_servo_angle(0)
            px.forward(30)
        case "backward":
            px.set_dir_servo_angle(0)
            px.backward(30)
        case "left":
            px.set_dir_servo_angle(-35)
            px.forward(30)
        case "right":
            px.set_dir_servo_angle(35)
            px.forward(30)
        case "backward_left":
            px.set_dir_servo_angle(-35)
            px.backward(30)
        case "backward_right":
            px.set_dir_servo_angle(35)
            px.backward(30)
        case "stop":
            px.stop()

def avoid_obstacle(left, right):
    if left > right:
        px.set_dir_servo_angle(-35)  # turn left
    else:
        px.set_dir_servo_angle(35)  # turn right
    px.forward(30)  
    time.sleep(1)  # let the robot move forward for 0.5 seconds (turn left or right)
    px.set_dir_servo_angle(0)  # straighten the wheel
Threshold = 30
if __name__ == "__main__":
    try:
        while True:
            distance = get_distance()
            if distance > Threshold:
                move_forward(30)
            else:
                px.set_dir_servo_angle(45)  # turn right
                px.forward(30)
                time.sleep(1)
            time.sleep(0.1)
    finally:
        px.stop()
        px.set_dir_servo_angle(0)
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
    
        
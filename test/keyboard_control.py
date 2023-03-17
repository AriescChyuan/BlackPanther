import mavlink_func as mav
import keyboard
import time
vehicle = mav.Mavlink("udpin:127.0.0.1:14551")
vehicle.vehicle.wait_heartbeat()
print(f"System:{vehicle.system}, component:{vehicle.component}")



while True:
    if keyboard.is_pressed('up'):
        vehicle.set_rc_channel_pwm(2,1400)
        print("forward")
    elif keyboard.is_pressed('down'):
        vehicle.set_rc_channel_pwm(2, 1600)
        print("back")
    elif keyboard.is_pressed('left'):
        vehicle.set_rc_channel_pwm(1, 1400)
        print("left")
    elif keyboard.is_pressed('right'):
        vehicle.set_rc_channel_pwm(1, 1600)
        print("right")
    elif keyboard.is_pressed('a'):
        vehicle.set_rc_channel_pwm(4, 1400)
        print("yaw left")
    elif keyboard.is_pressed('d'):
        vehicle.set_rc_channel_pwm(4, 1600)
        print("yaw right")
    elif keyboard.is_pressed('c'):
        break
    else:
        vehicle.set_rc_channel_pwm(1, 1500)
        vehicle.set_rc_channel_pwm(2, 1500)
        # vehicle.set_rc_channel_pwm(3, 1500)
        vehicle.set_rc_channel_pwm(4, 1500)
    time.sleep(0.1)
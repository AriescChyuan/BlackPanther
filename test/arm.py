import mavlink_func as mav
import time
vehicle = mav.Mavlink("udpin:127.0.0.1:14551")
vehicle.vehicle.wait_heartbeat()
print(f"System:{vehicle.system}, component:{vehicle.component}")

if __name__ == "__main__":
    vehicle.arm_disarm(1)
    time.sleep(5)
    vehicle.arm_disarm(0)
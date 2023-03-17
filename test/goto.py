import mavlink_func as mav
import time
vehicle = mav.Mavlink("udpin:127.0.0.1:14551")
vehicle.vehicle.wait_heartbeat()
print(f"System:{vehicle.system}, component:{vehicle.component}")

Target = {'latitude':24.1075579,'longitude':120.5911919,'altitude':10}

if __name__ == "__main__":
    vehicle.arm_disarm(1)
    time.sleep(5)
    vehicle.takeoff(10)
    time.sleep(1)

    while True:
        goto_check = input("是否飛行至指定點? Y/N :")
        if goto_check == 'Y':
            vehicle.goto(Target)
            break
        elif goto_check == 'N':
            print("取消飛行。")
            vehicle.set_mode("LAND")
            break
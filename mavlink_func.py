import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
import time
import geopy.distance
class Mavlink():

    system = ""
    component =""
    vehicle=""

    def __init__(self, device):
        vehicle  = utility.mavlink_connection(device=device)
        vehicle.wait_heartbeat()
        print("物件建立完成。")
        self.vehicle = vehicle
        self.system = vehicle.target_system
        self.component = vehicle.target_component
    
    def get_param(self,param):
        para_req_msg = dialect.MAVLink_param_request_read_message(
            target_system=self.system,
            target_component=self.component,
            param_id=param.encode("UTF-8"),
            param_index=-1,
        )
        self.vehicle.mav.send(para_req_msg)

    def set_param(self, param, value):
        param_set_msg = dialect.MAVLink_param_set_message(
            target_system=self.system,
            target_component=self.component,
            param_id=param.encode("utf-8"),
            param_value=value,
            param_type=dialect.MAV_PARAM_TYPE_REAL32
        )
        self.vehicle.mav.send(param_set_msg)

        message = self.vehicle.recv_match(type=dialect.MAVLink_param_value_message.msgname, blocking=True)
        message = message.to_dict()
        print(f"Set param {param} to {message['param_value']}")

    def set_mode(self, mode):
        flight_modes = self.vehicle.mode_mapping()

        if mode not in flight_modes.keys():
            print(mode,"is not supported!")
            print("You can try:",list(flight_modes.keys()))
            exit(1)
        else:
            set_mode_msg = dialect.MAVLink_command_long_message(
                target_system=self.system,
                target_component=self.component,
                command=dialect.MAV_CMD_DO_SET_MODE,
                confirmation=0,
                param1=dialect.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                param2=flight_modes[mode],
                param3=0,
                param4=0,
                param5=0,
                param6=0,
                param7=0
            )
        self.vehicle.mav.send(set_mode_msg)
        
        msg = self.vehicle.recv_match(type=dialect.MAVLink_command_ack_message.msgname, blocking=True)
        msg = msg.to_dict()
        if msg["command"] == dialect.MAV_CMD_DO_SET_MODE:
            if msg["result"] == dialect.MAV_RESULT_ACCEPTED:

                print(f"mode change to {mode} accepted")
                return "accepted"
            else:

                print("mode change denied")
                return "denied"
    def arm_disarm(self, value):
        arm_msg = dialect.MAVLink_command_long_message(
            target_system=self.system,
            target_component=self.component,
            command=dialect.MAV_CMD_COMPONENT_ARM_DISARM,
            confirmation=0,
            param1=value,
            param2=0,
            param3=0,
            param4=0,
            param5=0,
            param6=0,
            param7=0
        )
        self.vehicle.mav.send(arm_msg)

        msg = self.vehicle.recv_match(type=dialect.MAVLink_command_ack_message.msgname, blocking=True)
        msg = msg.to_dict()
    
        if value ==1:
            if msg["command"] == dialect.MAV_CMD_COMPONENT_ARM_DISARM:
                if msg["result"] == dialect.MAV_RESULT_ACCEPTED:
                    print("Vehcile is arm!!")
                else:
                    print("Vehcile is not arm!!")
        else:
            if msg["command"] == dialect.MAV_CMD_COMPONENT_ARM_DISARM:
                if msg["result"] == dialect.MAV_RESULT_ACCEPTED:
                    print("Vehcile is disarm!!")
                else:
                    print("Vehcile is not disarm!!")

    def hearth_check(self):
        msg = self.vehicle.recv_match(type=dialect.MAVLink_sys_status_message.msgname, blocking=True)
        msg = msg.to_dict()
        onboard_control_sensors_health = msg["onboard_control_sensors_health"]
        prearm_status_bit = onboard_control_sensors_health & dialect.MAV_SYS_STATUS_PREARM_CHECK
        prearm_status = prearm_status_bit == dialect.MAV_SYS_STATUS_PREARM_CHECK
        return prearm_status

    def takeoff(self, height):
        takeoff_msg = dialect.MAVLink_command_long_message(
            target_system=self.system,
            target_component=self.component,
            command=dialect.MAV_CMD_NAV_TAKEOFF,
            confirmation=0,
            param1=0,
            param2=0,
            param3=0,
            param4=0,
            param5=0,
            param6=0,
            param7=height
        )
        self.vehicle.mav.send(takeoff_msg)
        print("Takeoff....")
        while True:
            msg = self.vehicle.recv_match(type=dialect.MAVLink_global_position_int_message.msgname, blocking=True)
            msg = msg.to_dict()
            relative_alt = msg["relative_alt"] * 1e-3
        
            if height - relative_alt < 1:
                print(f"Takeoff to : {height} meters is successful!")
                break
            # else:
            #     print(f"current alt is : {relative_alt} meter.")
            #     time.sleep(1)
    
    def goto(self, location):
        target_msg = dialect.MAVLink_mission_item_int_message(
            target_system=self.system,
            target_component=self.component,
            seq=0,
            frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            command=dialect.MAV_CMD_NAV_WAYPOINT,
            current=2,
            autocontinue=0,
            param1=0,
            param2=0,
            param3=0,
            param4=0,
            x=int(location["latitude"] * 1e7),
            y=int(location["longitude"] * 1e7),
            z=location["altitude"]
            )
        self.vehicle.mav.send(target_msg)
        print("Go to target!")
        
    
    


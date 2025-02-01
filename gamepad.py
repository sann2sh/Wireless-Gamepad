import serial
import serial.tools.list_ports
import vgamepad as vg
import struct

#Put your arduino vid and pid, to get vid and pid connect your arduino and run this code, the vid and pid will be printed.
ARDUINO_VID = 6790 #vid for arduino nano
ARDUINO_PID = 29987 #pid for arduino nano

def find_arduino():
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        print(f"Detected: {port.device} - {port.description} (VID: {port.vid}, PID: {port.pid})")

        if (port.vid == ARDUINO_VID and port.pid == ARDUINO_PID) or "CH340" in port.description:
            print(f"Using CH340 Arduino on {port.device}")
            return port.device
        
    print("No CH340 Arduino found.")
    return None


arduino_port = find_arduino()
if not arduino_port:
    exit()  

baud_rate = 115200
gamepad = vg.VX360Gamepad()
ser = serial.Serial(arduino_port, baud_rate, timeout=0)

struct_format = 'HHHHHHHHHHHHH'
struct_size = struct.calcsize(struct_format)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def read_packet():
    while True:
        if ser.in_waiting > 0:
            byte = ser.read(1)
            if byte == b'<':
                packet = ser.read(struct_size)
                end_byte = ser.read(1)
                if end_byte == b'>':
                    return packet

while True:
    packet = read_packet()
    x = 0
    (vp1, vp2, vj1x, vj1y, vj2x, vj2y,
     vtg1, vtg2, vj2s, vs1, vs2, vs3, vs4) = struct.unpack(struct_format, packet)
    
    left_y = map_value(vj2x, 0, 1023, -1.0, 1.0)
    left_x = map_value(vj2y, 0, 1023, -1.0, 1.0)
    right_y = map_value(x, 0, 1023, -1.0, 1.0)
    right_x = map_value(x, 0, 1023, -1.0, 1.0)

    left_trigger = int(map_value(vj1x, 0, 512, 255, 0))
    right_trigger = int(map_value(vj2x, 512, 1023, 0, 255))
    
    gamepad.left_joystick_float(left_x, left_y)
    gamepad.right_joystick_float(right_x, right_y)
    gamepad.left_trigger(value=left_trigger)
    gamepad.right_trigger(value=right_trigger)
    
    vs1, vs2, vs3, vs4, vtg1, vtg2, vj2s = [1 - val for val in [vs1, vs2, vs3, vs4, vtg1, vtg2, vj2s]]

    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A) if vj2s else gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B) if vs3 else gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X) if vs1 else gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y) if vs2 else gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER) if vtg1 else gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER) if vtg2 else gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB) if vs4 else gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
    
    gamepad.update()

import serial
import vgamepad as vg
import struct
import time


arduino_port = 'COM6'  # replace with your port
baud_rate = 115200

gamepad = vg.VX360Gamepad() #gamepad emulater

ser = serial.Serial(arduino_port, baud_rate, timeout=0)

# struct format for unpacking the 2-byte unsigned int data (13 values) sent by arduino
struct_format = 'HHHHHHHHHHHHH'
struct_size = struct.calcsize(struct_format)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def read_packet():

    while True:
        if ser.in_waiting > 0:
            byte = ser.read(1)
            if byte == b'<':  # Start marker for data synchronization
                packet = ser.read(struct_size)  # Read the struct
                end_byte = ser.read(1)  # Read the end marker
                if end_byte == b'>':  # End marker
                    return packet


while True:
    packet = read_packet()

    # Unpack the data
    (vp1, vp2, vj1x, vj1y, vj2x, vj2y,
     vtg1, vtg2, vj2s, vs1, vs2, vs3, vs4) = struct.unpack(struct_format, packet)

    # Map the joystick values to the range -1.0 to 1.0
    left_y = map_value(vj1x, 0, 1023, -1.0, 1.0)
    left_x = map_value(vj1y, 0, 1023, -1.0, 1.0)
    right_y = map_value(vj2x, 0, 1023, -1.0, 1.0)
    right_x = map_value(vj2y, 0, 1023, -1.0, 1.0)

    # Map the trigger values to the range 0 to 255
    left_trigger = int(map_value(vp1, 0, 1023, 0, 255))
    right_trigger =int(map_value(vp2, 0, 1023, 0, 255))

    # Set the joystick positions
    gamepad.left_joystick_float(left_x, left_y)
    gamepad.right_joystick_float(right_x, right_y)

    # Set the trigger values
    gamepad.left_trigger(value=left_trigger)
    gamepad.right_trigger(value=right_trigger)

    # Invert the button states (0 when pressed, 1 when not pressed)
    vs1 = 1 - vs1
    vs2 = 1 - vs2
    vs3 = 1 - vs3
    vs4 = 1 - vs4
    vtg1 = 1 - vtg1
    vtg2 = 1 - vtg2
    vj2s = 1 - vj2s

    # Set the button states
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A) if vj2s else gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B) if vs3 else gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X) if vs1 else gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y) if vs2 else gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER) if vtg1 else gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER) if vtg2 else gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB) if vs4 else gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)

    # Update gamepad state
    gamepad.update()

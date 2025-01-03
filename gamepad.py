import serial
import vgamepad as vg
import time

# Create a virtual gamepad
gamepad = vg.VX360Gamepad()

# Open the serial port
arduino = serial.Serial('COM4', 115200, timeout=.1)


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:
    if arduino.inWaiting() > 0:
        rawdata = arduino.readline()
        data = rawdata.decode('utf-8').strip()
        v = data.split(',')

        if len(v) >= 13:
            try:
                vp1 = int(v[0])
                vp2 = int(v[1])
                vj1x = int(v[2])
                vj1y = int(v[3])
                vj2x = int(v[4])
                vj2y = int(v[5])
                vtg1 = int(v[6])
                vtg2 = int(v[7])
                vj2s = int(v[8])
                vs1 = int(v[9])
                vs2 = int(v[10])
                vs3 = int(v[11])
                vs4 = int(v[12])

                # Map the joystick values to the range -1.0 to 1.0
                left_y = map_value(vj1x, 0, 32768, -1.0, 1.0)
                left_x = map_value(vj1y, 0, 32768, -1.0, 1.0)
                right_y = map_value(vj2x, 0, 32768, -1.0, 1.0)
                right_x = map_value(vj2y, 0, 32768, -1.0, 1.0)

                # Map the trigger values to the range 0 to 255
                left_trigger = 0 if vp1 < 28000 else int(map_value(vp1, 28000, 32768, 0, 255))
                right_trigger = 0 if vp2 < 28000 else int(map_value(vp2, 28000, 32768, 0, 255))

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
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A) if vs4 else gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B) if vs3 else gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X) if vs2 else gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y) if vj2s else gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER) if vtg1 else gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER) if vtg2 else gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB) if vs1 else gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)

                # Update the virtual gamepad state
                gamepad.update()

            except ValueError as e:
                print(f"Error parsing values: {e}")
        else:
            print(f"Received incomplete data: {data}")

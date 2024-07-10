import time
import board
import digitalio
import keypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Button class
class Button:
    BUTTON_W = 0
    BUTTON_A = 1
    BUTTON_S = 2
    BUTTON_D = 3
    BUTTON_I = 4
    BUTTON_J = 5
    BUTTON_K = 6
    BUTTON_L = 7

    MC_BUTTON_W = board.GP5
    MC_BUTTON_A = board.GP6
    MC_BUTTON_S = board.GP7
    MC_BUTTON_D = board.GP8
    MC_BUTTON_I = board.GP12
    MC_BUTTON_J = board.GP13
    MC_BUTTON_K = board.GP14
    MC_BUTTON_L = board.GP15

# Set up the onboard LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set up buttons
buttons = keypad.Keys(
    pins=(Button.MC_BUTTON_W, Button.MC_BUTTON_A, Button.MC_BUTTON_S, Button.MC_BUTTON_D,
          Button.MC_BUTTON_I, Button.MC_BUTTON_J, Button.MC_BUTTON_K, Button.MC_BUTTON_L),
    value_when_pressed=False,
    pull=True
)

# Set up USB HID keyboard
keyboard = Keyboard(usb_hid.devices)

# Define key mappings
key_mapping = {
    Button.BUTTON_W: Keycode.W,
    Button.BUTTON_A: Keycode.A,
    Button.BUTTON_S: Keycode.S,
    Button.BUTTON_D: Keycode.D,
    Button.BUTTON_I: Keycode.UP_ARROW,  # Changed to UP_ARROW
    Button.BUTTON_J: Keycode.G,         # Changed to G
    Button.BUTTON_K: Keycode.DOWN_ARROW,  # Changed to DOWN_ARROW
    Button.BUTTON_L: Keycode.E          # Changed to E
}

print('USB HID Keyboard emulation active')

last_button_state = [1] * 8
led_state = False
last_blink_time = time.monotonic()

while True:
    current_time = time.monotonic()
    
    # Blink LED every 0.5 seconds
    if current_time - last_blink_time >= 0.5:
        led_state = not led_state
        led.value = led_state
        last_blink_time = current_time

    events = buttons.events.get()
    if events:
        while events:
            if events.pressed:
                keyboard.press(key_mapping[events.key_number])
            elif events.released:
                keyboard.release(key_mapping[events.key_number])
            events = buttons.events.get()
    
    time.sleep(0.01)
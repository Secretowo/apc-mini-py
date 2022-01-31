# apc-mini-py
Interface with an AKAI APC Mini MIDI controller using python

Requires [mido](https://github.com/mido/mido)

# Usage:

```python

from apc_mini_py import apcmini

# apc = ApcMini(midi_in=None, midi_out=None)
apc = apcmini.APCMini('APC MINI 0', 'APC MINI 1')

apc.reset()  # turn off all leds

# NOTE: All buttons are indexed from 0!

# apc.gridbuttons.set(x, y, colour) set color of an LED on the button grid
apc.gridbuttons.set_led(0, 0, "red")
apc.gridbuttons.set_led(0, 1, 4)
# sending raw values is probably faster but they're harder to remember.

# apc.sidebuttons.set_led(id, colour) sets the colour of an LED on the side buttons
apc.sidebuttons.set_led(0, "green_blinking")

# apc.lowerbuttons.set_led(id, colour) sets the colour of an LED on the lower buttons
apc.lowerbuttons.set_led(3, "red")


# Function that is called when a button is pressed or fader is changed
@apc.on_event
def on_button_press(event):
    # Can be Fader, SideButton, LowerButton or GridButton class
    # isinstance() can be used to filter out a specific action for a specific button press (liek below)

    if isinstance(event, apcmini.GridButton):
        print(f"Button {event.x},{event.y} was pressed on the grid!")
    elif isinstance(event, apcmini.LowerButton):
        print(f"Button {event.button_id} was pressed on {event.controller.name}")
    elif isinstance(event, apcmini.Fader):
        print(f"Fader {event.fader_id} on {event.controller.name} was set to {event.value}!")


apc.start()  # Starts the event loop for button/fader interactions, not required for LED control
```

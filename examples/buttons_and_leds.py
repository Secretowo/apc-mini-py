from apc_mini_py import apcmini
from scipy.interpolate import interp1d

# apc = ApcMini(midi_in=None, midi_out=None)
apc = apcmini.APCMini('APC MINI MIDI 1', 'APC MINI MIDI 1')

midi_to_led = interp1d([0, 127], [0, 7])  # Creates a map from the 7 bit values of MIDI to a 3 bit value for display

apc.reset()  # turn off all leds


# Defines this function for recieving button presses/fader changes
@apc.on_event
def on_control_event(event):
    if isinstance(event, apcmini.GridButton):  # Checks if the event is a grid button press
        if event.state:
            apc.gridbuttons.set_led(event.x, event.y, "red")  # Turn the button red when pressed
        else:
            apc.gridbuttons.set_led(event.x, event.y, "off")  # and off when not pressed
    elif isinstance(event, apcmini.Fader):
        if event.fader_id == 8:  # Ignore fader ID 8 (the master fader)
            return
        value = int(midi_to_led(event.value))  # Map the MIDI value (0,127) to 3 bit (0,7)
        if value == 0:  # If the value is 0 (fader at minimum)
            for i in range(0, 8):
                apc.gridbuttons.set_led(event.fader_id, i, "off")  # Set all LEDs in the column to off
        elif value == 7:  # If the value is 7 (fader at maximum)
            for i in range(0, 8):
                apc.gridbuttons.set_led(event.fader_id, i, "green")  # Set all LEDs in column to green
        else:
            for i in range(0, value):  # Go through all the LEDs that should be on
                apc.gridbuttons.set_led(event.fader_id, i, "green")  # and set them to green
            for i in range(value+1, 8):  # Go through all the LEDs that should be off
                apc.gridbuttons.set_led(event.fader_id, i, "off")   # and set them to off


apc.start()  # Starts the event loop

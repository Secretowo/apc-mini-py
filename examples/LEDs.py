from apc_mini_py import apcmini
import time

# apc = ApcMini(midi_in=None, midi_out=None)
apc = apcmini.APCMini('APC MINI MIDI 1', 'APC MINI MIDI 1')

apc.reset()  # turn off all leds

for x in range(0, 8):
    for y in range(0, 8):
        apc.gridbuttons.set_led(x, y, "red")
        time.sleep(0.005)


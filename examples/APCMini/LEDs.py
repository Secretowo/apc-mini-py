from akai_pro_py import controllers
import time

# apc = ApcMini(midi_in=None, midi_out=None)
apc = controllers.APCMini('Midi Through Port-0', 'Midi Through Port-0')

apc.reset()  # turn off all leds

for x in range(0, 8):
    for y in range(0, 8):
        apc.gridbuttons.set_led(x, y, "red")
        time.sleep(0.005)


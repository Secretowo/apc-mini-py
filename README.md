# apc-mini-py
Interface with an AKAI Apc Mini midi controller using python

Requires [mido](https://github.com/mido/mido)

# Usage:
```python
from apcmini import ApcMini


#apc = ApcMini(midi_in=None, midi_out=None)
apc = ApcMini('APC MINI 0', 'APC MINI 1')

apc.reset() #turn off all leds

#apc.set(button, state) set color of specific led
apc.set(0, "red")
apc.set(0, 1) # sending raw values is probably faster but theyre harder to remember.

#read button presses:
#(these are mido message objects)
for msg in apc.pending_inputs():
  print(msg)
```

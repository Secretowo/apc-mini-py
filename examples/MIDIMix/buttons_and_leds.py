from akai_pro_py import controllers

# Define the MIDI Mix and APC Mini, first argument: MIDI in, second argument: MIDI out
midi_mix = controllers.MIDIMix('MIDI Mix MIDI 1', 'MIDI Mix MIDI 1')

midi_mix.reset()


@midi_mix.on_event
def on_event_midi_mix(event):
    if isinstance(event, controllers.MIDIMix.Knob):
        print(f"Knob {event.x},{event.y} was changed to {event.value} on {event.controller.name}")
    if isinstance(event, controllers.MIDIMix.Fader):
        print(f"Fader {event.fader_id} was changed to {event.value} on {event.controller.name}")
    if isinstance(event, controllers.MIDIMix.MuteButton):
        print(f"Mute Button {event.button_id} was changed to {event.state} on {event.controller.name}")
        if event.state:
            event.set_led("on")
        else:
            event.set_led("off")
    if isinstance(event, controllers.MIDIMix.RecArmButton):
        print(f"Record Arm Button {event.button_id} was changed to {event.state} on {event.controller.name}")
        if event.state:
            event.set_led("on")
        else:
            event.set_led("off")
    if isinstance(event, controllers.MIDIMix.SoloButton):
        print(f"Solo Button was changed to {event.state} on {event.controller.name}")
    if isinstance(event, controllers.MIDIMix.BlankButton):
        print(f"Blank Button {event.button_id} was changed to {event.state} on {event.controller.name}")
        if event.state:
            event.set_led("on")
        else:
            event.set_led("off")


midi_mix.start()  # Start event loop

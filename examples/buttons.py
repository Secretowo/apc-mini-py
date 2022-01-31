import apcmini

# Define the APC Mini, first argument: MIDI in, second argument: MIDI out
apc = apcmini.APCMini('APC MINI MIDI 1', 'APC MINI MIDI 1')


# Defines this function for recieving button presses/fader changes
@apc.on_event
def on_control_event(event):
    # Can be Fader, SideButton, LowerButton or GridButton class
    # isinstance() can be used to filter out a specific action for a specific button press (liek below)

    if isinstance(event, apcmini.GridButton):
        print(f"Grid Button {event.x},{event.y} was changed to {event.state} on {event.controller.name}")
    elif isinstance(event, apcmini.LowerButton):
        print(f"Lower Button {event.button_id} was changed to {event.state} on {event.controller.name}")
    elif isinstance(event, apcmini.SideButton):
        print(f"Side Button {event.button_id} was changed to {event.state} on {event.controller.name}")
    elif isinstance(event, apcmini.Fader):
        print(f"Fader {event.fader_id} on {event.controller.name} was set to {event.value}!")


apc.start()  # Starts the event loop

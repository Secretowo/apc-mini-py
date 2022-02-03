from akai_pro_py import controllers

# Define the APC Mini, first argument: MIDI in, second argument: MIDI out
apc = controllers.APCMini('APC MINI MIDI 1', 'APC MINI MIDI 1')


# Defines this function for recieving button presses/fader changes
@apc.on_event
def on_control_event(event):
    # Can be Fader, SideButton, LowerButton or GridButton class
    # isinstance() can be used to filter out a specific action for a specific button press (liek below)

    if isinstance(event, controllers.APCMini.GridButton):
        print(f"Grid Button {event.x},{event.y} was changed to {event.state} on {event.controller.name}")
    elif isinstance(event, controllers.APCMini.LowerButton):
        print(f"Lower Button {event.button_id} was changed to {event.state} on {event.controller.name}")
    elif isinstance(event, controllers.APCMini.SideButton):
        print(f"Side Button {event.button_id} was changed to {event.state} on {event.controller.name}")
    elif isinstance(event, controllers.APCMini.ShiftButton):
        print(f"Shift Button was changed to {event.state} on {event.controller.name}")
    elif isinstance(event, controllers.APCMini.Fader):
        print(f"Fader {event.fader_id} on {event.controller.name} was set to {event.value}!")


apc.start()  # Starts the event loop

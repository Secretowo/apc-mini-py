import mido
import asyncio


class Controller:
    def __init__(self, midi_in=None, midi_out=None):
        self.midi_out = mido.open_output(midi_out)  # Open MIDI out for controller
        self.midi_in = mido.open_input(midi_in)  # Open MIDI in for controller
        self.setup_in_progress = True
        self.midi_in.callback = self.pre_event_dispatch  # Set callback function for incomming MIDI messages
        self.event_dispatch = None  # Defines the dispatch event to be none
        self.loop = asyncio.new_event_loop()  # Creates the event loop for handling button presses
        self.name = "Base Controller"  # Name of the device
        self.midi_out.send(mido.Message.from_bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7]))

    def on_event(self, func):
        """Used to dispatch MIDI events from APC Mini"""
        if self.event_dispatch is not None:
            raise ValueError("Event dispatch function is already defined!")
        self.event_dispatch = func

    def pre_event_dispatch(self, event):
        if self.setup_in_progress:
            if event.data[4] != 71:
                raise ValueError("MIDI device is not an Akai device!")
        if self.event_dispatch is None:
            return  # Ignore if a dispatch event is not set with the on_event decorator

    def start(self):
        """Start the event loop for receiving MIDI messages"""
        self.loop.run_forever()


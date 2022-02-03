class AkaiProPyError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return "Generic Akai Pro Py error"


class ControllerError(AkaiProPyError):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Generic controller error"

    def __str__(self):
        if self.message:
            return f'Controller Error: {self.message}'
        else:
            return ''


class ControllerIdentificationError(ControllerError):
    def __init__(self, *args):
        if args:
            self.controller = args[0]
            self.midi_port = args[1]
            self.message = args[2]
        else:
            self.controller = None
            self.midi_port = None
            self.message = "Generic controller identification error"

    def __str__(self):
        if self.controller and self.midi_port:
            return f"{self.controller.name} on MIDI port '{self.midi_port.name}': {self.message}"
        else:
            return "Generic Controller Identification Error"


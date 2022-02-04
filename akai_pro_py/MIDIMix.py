from .base_controller import Controller
import mido
import time
from . import errors


class InvalidKnob(errors.ControllerError):
    def __init__(self, *args):
        if args:
            self.controller = args[0]
            self.midi_port = args[1]
            if isinstance(args[2], tuple):
                self.x, self.y = args[2]
                self.button_id = None
            else:
                self.x, self.y = (None, None)
                self.button_id = args[2]
        else:
            self.controller = None
            self.midi_port = None
            self.x, self.y = (None, None)

    def __str__(self):
        if self.controller and self.midi_port and self.x and self.y:
            return f"Knob {self.x},{self.y} does not exist on controller {self.controller.name}, MIDI port: {self.midi_port.name}"
        elif self.controller and self.midi_port and self.button_id:
            return f"Knob {self.button_id} does not exist on controller {self.controller.name}, MIDI port: {self.midi_port.name}"
        elif not self.controller and not self.midi_port and self.x and self.y:
            return f"Knob {self.x},{self.y} does not exist on controller"
        elif not self.controller and not self.midi_port and self.button_id:
            return f"Knob {self.button_id} does not exist on controller"
        else:
            return "Generic invalid knob coordinate error"


class InvalidRecArmButton(errors.ControllerError):
    def __init__(self, *args):
        if args:
            self.controller = args[0]
            self.midi_port = args[1]
            self.button_id = args[2]
        else:
            self.controller = None
            self.midi_port = None
            self.button_id = None

    def __str__(self):
        if self.controller and self.midi_port and self.button_id:
            return f"Record Arm button {self.button_id} does not exist on controller {self.controller.name}, MIDI port: {self.midi_port.name}"
        elif not self.controller and not self.midi_port and self.button_id:
            return f"Record Arm button {self.button_id} does not exist on controller"
        else:
            return "Generic invalid Record Arm button error"


class InvalidMuteButton(errors.ControllerError):
    def __init__(self, *args):
        if args:
            self.controller = args[0]
            self.midi_port = args[1]
            self.button_id = args[2]
        else:
            self.controller = None
            self.midi_port = None
            self.button_id = None

    def __str__(self):
        if self.controller and self.midi_port and self.button_id:
            return f"Mute button {self.button_id} does not exist on controller {self.controller.name}, MIDI port: {self.midi_port.name}"
        elif not self.controller and not self.midi_port and self.button_id:
            return f"Mute button {self.button_id} does not exist on controller"
        else:
            return "Generic invalid Mute button error"


class InvalidBlankButton(errors.ControllerError):
    def __init__(self, *args):
        if args:
            self.controller = args[0]
            self.midi_port = args[1]
            self.button_id = args[2]
        else:
            self.controller = None
            self.midi_port = None
            self.button_id = None

    def __str__(self):
        if self.controller and self.midi_port and self.button_id:
            return f"Blank button {self.button_id} does not exist on controller {self.controller.name}, MIDI port: {self.midi_port.name}"
        elif not self.controller and not self.midi_port and self.button_id:
            return f"Blank button {self.button_id} does not exist on controller"
        else:
            return "Generic invalid Blank button error"


class InvalidButtonColour(errors.ControllerError):
    def __init__(self, *args):
        if args:
            self.controller = args[0]
            self.midi_port = args[1]
            self.button = args[2]
        else:
            self.controller = None
            self.midi_port = None
            self.button = None

    def __str__(self):
        if isinstance(self.button, MIDIMix.MuteButton):
            return f"Invalid button colour for Mute button, valid options are 0,1,on,off,yellow"
        elif isinstance(self.button, MIDIMix.RecArmButton):
            return f"Invalid button colour for Record Arm button, valid options are 0,1,on,off,red"
        elif isinstance(self.button, MIDIMix.BlankButton):
            return f"Invalid button colour for Blank button, valid options are 0,1,on,off,yellow"
        else:
            return "Generic invalid button colour error"


class InvalidFader(errors.ControllerError):
    def __init__(self, *args):
        if args:
            self.controller = args[0]
            self.midi_port = args[1]
            self.fader_id = args[2]
        else:
            self.controller = None
            self.midi_port = None
            self.fader_id = None

    def __str__(self):
        if self.controller and self.midi_port and self.fader_id:
            return f"Fader {self.fader_id} does not exist on controller {self.controller.name}, MIDI port: {self.midi_port.name}"

        elif not self.controller and not self.midi_port and self.button_id:
            return f"Fader {self.fader_id} does not exist on controller"

        else:
            return "Generic invalid Fader error"


class MIDIMix(Controller):
    KnobGridMapping = [
        [18, 17, 16],
        [22, 21, 20],
        [26, 25, 24],
        [30, 29, 28],
        [48, 47, 46],
        [52, 51, 50],
        [56, 55, 54],
        [60, 59, 58]
    ]  # Mapping of the 8x3 grid of knobs
    Knobs = [18, 17, 16, 22, 21, 20, 26, 25, 24, 30, 29, 28, 48, 47, 46, 52, 51, 50, 56, 55, 54, 60, 59, 58]

    FaderMapping = [19, 23, 27, 31, 49, 53, 57, 61, 62]  # Mapping of faders to their number indexed from 0

    RecArmMapping = [3, 6, 9, 12, 15, 18, 21, 24]
    RecArmColours = {
        "off": 0,
        "red": 1,
        "on": 1
    }

    MuteMapping = [1, 4, 7, 10, 13, 16, 19, 22]
    MuteColours = {
        "off": 0,
        "yellow": 1,
        "on": 1
    }

    BlankMapping = [26, 25]
    BlankColours = {
        "off": 0,
        "yellow": 1,
        "on": 1
    }

    SoloMapping = [27]

    def __init__(self, midi_in=None, midi_out=None):
        super().__init__(midi_in, midi_out)
        self.name = "Akai MIDI Mix"  # Name of the device
        self.mutebuttons = MIDIMix.MuteButtons(self)
        self.recarmbuttons = MIDIMix.RecArmButtons(self)
        self.blankbuttons = MIDIMix.BlankButtons(self)

    def product_detect(self, event):
        try:
            if event.data[2] != 6:
                raise errors.ControllerIdentificationError(self, self.midi_in, "Controller did not identify!")

            if event.data[4] != 71:
                raise errors.ControllerIdentificationError(self, self.midi_in, "MIDI device is not an Akai device!")

            if event.data[5] != 49:
                raise errors.ControllerIdentificationError(self, self.midi_in, "MIDI device is not an Akai MIDI Mix")
                          
        except (AttributeError, KeyError):
            raise errors.ControllerIdentificationError(self, self.midi_in, "MIDI device failed to identify")
        self.setup_in_progress = False
        return True

    def pre_event_dispatch(self, event):
        if self.event_dispatch is None:
            return  # Ignore if a dispatch event is not set with the on_event decorator

        if event.type == "control_change":  # Event is a fader or knob change
            if event.control in MIDIMix.FaderMapping:
                fader = MIDIMix.Fader(self, MIDIMix.Fader.get_fader_id_from_number(event.control), event.value)
                self.event_dispatch(fader)
            elif event.control in MIDIMix.Knobs:
                knob = MIDIMix.Knob(self, *MIDIMix.Knob.get_knob_xy_from_number(event.control), event.value)
                self.event_dispatch(knob)

        elif event.type == "note_on" or event.type == "note_off":
            if event.note in MIDIMix.RecArmMapping:
                if event.type == "note_on":
                    button = MIDIMix.RecArmButton(self, MIDIMix.RecArmButton.get_button_id_from_button_num(event.note),
                                                  True)
                    self.event_dispatch(button)
                elif event.type == "note_off":
                    button = MIDIMix.RecArmButton(self, MIDIMix.RecArmButton.get_button_id_from_button_num(event.note),
                                                  False)
                    self.event_dispatch(button)

            elif event.note in MIDIMix.MuteMapping:
                if event.type == "note_on":
                    button = MIDIMix.MuteButton(self, MIDIMix.MuteButton.get_button_id_from_button_num(event.note),
                                                True)
                    self.event_dispatch(button)
                elif event.type == "note_off":
                    button = MIDIMix.MuteButton(self, MIDIMix.MuteButton.get_button_id_from_button_num(event.note),
                                                False)
                    self.event_dispatch(button)

            elif event.note in MIDIMix.BlankMapping:
                if event.type == "note_on":
                    button = MIDIMix.BlankButton(self, MIDIMix.BlankButton.get_button_id_from_button_num(event.note),
                                                 True)
                    self.event_dispatch(button)
                elif event.type == "note_off":
                    button = MIDIMix.BlankButton(self, MIDIMix.BlankButton.get_button_id_from_button_num(event.note),
                                                 False)
                    self.event_dispatch(button)

            elif event.note in MIDIMix.SoloMapping:
                if event.type == "note_on":
                    button = MIDIMix.SoloButton(self, True)
                    self.event_dispatch(button)
                elif event.type == "note_off":
                    button = MIDIMix.SoloButton(self, False)
                    self.event_dispatch(button)

    def reset(self):
        for ButtonGroup in [MIDIMix.MuteMapping, MIDIMix.RecArmMapping, MIDIMix.BlankMapping]:
            for Button in ButtonGroup:
                self.midi_out.send(
                    mido.Message("note_on", note=Button, velocity=0))
                time.sleep(0.005)

    class Fader:
        def __init__(self, controller, fader_id, value):
            self.controller = controller
            self.fader_id = fader_id
            self.value = value

        @staticmethod
        def get_fader_id_from_number(fader_num):
            try:
                return MIDIMix.FaderMapping.index(fader_num)
            except IndexError:
                raise InvalidFader(None, None, fader_num)

    class Knob:
        def __init__(self, controller, x, y, value):
            self.controller = controller
            self.x = x
            self.y = y
            self.value = value

        @staticmethod
        def get_knob_xy_from_number(knob_num):
            for column in MIDIMix.KnobGridMapping:
                x = MIDIMix.KnobGridMapping.index(column)
                if knob_num in column:
                    return x, MIDIMix.KnobGridMapping[x].index(knob_num)
                else:
                    continue
            raise InvalidKnob(None, None, knob_num)

    class MuteButtons:  # All the lower buttons
        def __init__(self, controller):
            self.controller = controller

        def set_led(self, button_id, colour):
            """Sets an LED on the lower buttons"""
            MIDIMix.MuteButton(self.controller, button_id).set_led(colour)

    class MuteButton:  # A specific side button
        def __init__(self, controller, button_id: int, state: bool = False):
            self.controller = controller
            self.button_id = button_id
            self.state = state

        @staticmethod
        def get_button_id_from_button_num(button_num):
            try:
                return MIDIMix.MuteMapping.index(button_num)
            except IndexError:
                raise InvalidMuteButton(None, None, button_num)

        def set_led(self, colour):
            """Sets this specific button's LED to be the colour given"""
            if isinstance(colour, int):
                if 0 <= colour <= 1:
                    try:
                        self.controller.midi_out.send(
                            mido.Message("note_on", note=MIDIMix.MuteMapping[self.button_id], velocity=colour))
                    except IndexError:
                        raise InvalidMuteButton(self.controller, self.controller.midi_in, self.button_id)
                else:
                    raise InvalidButtonColour(self.controller, self.controller.midi_in, self)
            else:
                if colour in MIDIMix.MuteColours:
                    try:
                        self.controller.midi_out.send(
                            mido.Message("note_on", note=MIDIMix.MuteMapping[self.button_id],
                                         velocity=MIDIMix.MuteColours[colour]))
                    except IndexError:
                        raise InvalidMuteButton(self.controller, self.controller.midi_in, self.button_id)
                else:
                    raise InvalidButtonColour(self.controller, self.controller.midi_in, self)

    class RecArmButtons:  # All the lower buttons
        def __init__(self, controller):
            self.controller = controller

        def set_led(self, button_id, colour):
            """Sets an LED on the lower buttons"""
            MIDIMix.RecArmButton(self.controller, button_id).set_led(colour)

    class RecArmButton:  # A specific side button
        def __init__(self, controller, button_id: int, state: bool = False):
            self.controller = controller
            self.button_id = button_id
            self.state = state

        @staticmethod
        def get_button_id_from_button_num(button_num):
            try:
                return MIDIMix.RecArmMapping.index(button_num)
            except:
                raise InvalidRecArmButton(None, None, button_num)

        def set_led(self, colour):
            """Sets this specific button's LED to be the colour given"""
            if isinstance(colour, int):
                if 0 <= colour <= 1:
                    try:
                        self.controller.midi_out.send(
                            mido.Message("note_on", note=MIDIMix.RecArmMapping[self.button_id], velocity=colour))
                    except IndexError:
                        raise InvalidRecArmButton(self.controller, self.controller.midi_in, self.button_id)
                else:
                    raise InvalidButtonColour(self.controller, self.controller.midi_in, self)
            else:
                if colour in MIDIMix.RecArmColours:
                    try:
                        self.controller.midi_out.send(
                            mido.Message("note_on", note=MIDIMix.RecArmMapping[self.button_id],
                                         velocity=MIDIMix.RecArmColours[colour]))
                    except IndexError:
                        raise InvalidRecArmButton(self.controller, self.controller.midi_in, self.button_id)
                else:
                    raise InvalidButtonColour(self.controller, self.controller.midi_in, self)

    class BlankButtons:  # All the lower buttons
        def __init__(self, controller):
            self.controller = controller

        def set_led(self, button_id, colour):
            """Sets an LED on the lower buttons"""
            MIDIMix.BlankButton(self.controller, button_id).set_led(colour)

    class BlankButton:  # A specific side button
        def __init__(self, controller, button_id: int, state: bool = False):
            self.controller = controller
            self.button_id = button_id
            self.state = state

        @staticmethod
        def get_button_id_from_button_num(button_num):
            try:
                return MIDIMix.BlankMapping.index(button_num)
            except IndexError:
                raise InvalidBlankButton(None, None, button_num)

        def set_led(self, colour):
            """Sets this specific button's LED to be the colour given"""
            if isinstance(colour, int):
                if 0 <= colour <= 1:
                    try:
                        self.controller.midi_out.send(
                            mido.Message("note_on", note=MIDIMix.BlankMapping[self.button_id], velocity=colour))
                    except IndexError:
                        raise InvalidBlankButton(self.controller, self.controller.midi_in, self.button_id)
                else:
                    raise InvalidButtonColour(self.controller, self.controller.midi_in, self)
            else:
                if colour in MIDIMix.RecArmColours:
                    try:
                        self.controller.midi_out.send(
                            mido.Message("note_on", note=MIDIMix.BlankMapping[self.button_id],
                                         velocity=MIDIMix.BlankColours[colour]))
                    except IndexError:
                        raise InvalidBlankButton(self.controller, self.controller.midi_in, self.button_id)
                else:
                    raise InvalidButtonColour(self.controller, self.controller.midi_in, self)

    class SoloButton:  # The shift button
        def __init__(self, controller, state: bool = False):
            self.controller = controller
            self.state = state

from .base_controller import Controller
import mido
import time


class APCMini(Controller):
    GridMapping = [
        [0, 8, 16, 24, 32, 40, 48, 56],
        [1, 9, 17, 25, 33, 41, 49, 57],
        [2, 10, 18, 26, 34, 42, 50, 58],
        [3, 11, 19, 27, 35, 43, 51, 59],
        [4, 12, 20, 28, 36, 44, 52, 60],
        [5, 13, 21, 29, 37, 45, 53, 61],
        [6, 14, 22, 30, 38, 46, 54, 62],
        [7, 15, 23, 31, 39, 47, 55, 63]
    ]  # The mapping of an XY coordinate to the MIDI note for the button grid

    GridColours = {
        "off": 0,
        "green": 1,
        "green_blinking": 2,
        "red": 3,
        "red_blinking": 4,
        "yellow": 5,
        "yellow_blinking": 6
    }  # Dict of all available colours for the grid

    FaderMapping = [48, 49, 50, 51, 52, 53, 54, 55, 56]  # Mapping of faders to their number indexed from 0

    SideButtonMapping = [82, 83, 84, 85, 86, 87, 88, 89]  # Mapping of side buttons from top to bottom, indexed from 0

    SideButtonColours = {
        "on": 1,
        "off": 0,
        "green": 1,
        "green_blinking": 2
    }  # Dict of all colours for the side buttons

    LowerButtonMapping = [64, 65, 66, 67, 68, 69, 70, 71]  # Mapping of lower buttons from left to right, indexed from 0

    LowerButtonColours = {
        "on": 1,
        "off": 0,
        "red": 1,
        "red_blinking": 2
    }  # Dict of all colours for the lower buttons

    ShiftButtonMapping = [98]

    def __init__(self, midi_in=None, midi_out=None):
        super().__init__(midi_in, midi_out)
        self.name = "Akai APC Mini"  # Name of the device
        self.gridbuttons = APCMini.GridButtons(self)
        self.sidebuttons = APCMini.SideButtons(self)
        self.lowerbuttons = APCMini.LowerButtons(self)

    def reset(self):
        """Turns off all LEDs"""
        for i in range(0, 89 + 1):
            self.midi_out.send(mido.Message("note_on", note=i, velocity=0))
            time.sleep(0.005)

    def pre_event_dispatch(self, event):
        if self.setup_in_progress:
            if event.data[4] != 71:
                raise ValueError("MIDI device is not an Akai device!")

            if event.data[5] != 40:
                raise ValueError("MIDI device is not an Akai APC Mini")
            self.setup_in_progress = False
            return

        if self.event_dispatch is None:
            return  # Ignore if a dispatch event is not set with the on_event decorator

        if event.type == "control_change":  # Event is a fader change
            fader = APCMini.Fader(self, APCMini.Fader.get_fader_id_from_number(event.control), event.value)
            self.event_dispatch(fader)

        elif event.type == "note_on" or event.type == "note_off":  # Event is a button press
            if event.note in range(0, 63 + 1):  # Button grid
                if event.type == 'note_on':
                    button = APCMini.GridButton(self, *APCMini.GridButton.get_xy_from_button_num(event.note), True)
                    self.event_dispatch(button)

                elif event.type == 'note_off':
                    button = APCMini.GridButton(self, *APCMini.GridButton.get_xy_from_button_num(event.note), False)
                    self.event_dispatch(button)

            elif event.note in APCMini.SideButtonMapping:  # Side buttons
                if event.type == 'note_on':
                    button = APCMini.SideButton(self, APCMini.SideButton.get_button_id_from_button_num(event.note),
                                                True)
                    self.event_dispatch(button)

                elif event.type == 'note_off':
                    button = APCMini.SideButton(self, APCMini.SideButton.get_button_id_from_button_num(event.note),
                                                False)
                    self.event_dispatch(button)

            elif event.note in APCMini.LowerButtonMapping:  # Lower buttons
                if event.type == 'note_on':
                    button = APCMini.LowerButton(self, APCMini.LowerButton.get_button_id_from_button_num(event.note),
                                                 True)
                    self.event_dispatch(button)

                elif event.type == 'note_off':
                    button = APCMini.LowerButton(self, APCMini.LowerButton.get_button_id_from_button_num(event.note),
                                                 False)
                    self.event_dispatch(button)

            elif event.note in APCMini.ShiftButtonMapping:
                if event.type == 'note_on':
                    button = APCMini.ShiftButton(self, True)
                    self.event_dispatch(button)

                elif event.type == 'note_off':
                    button = APCMini.ShiftButton(self, False)
                    self.event_dispatch(button)

    class GridButtons:  # All the grid buttons
        def __init__(self, controller):
            self.controller = controller

        def set_led(self, x, y, colour):
            """Sets an LED on the button grid"""
            APCMini.GridButton(self.controller, x, y).set_led(colour)

    class GridButton:  # A specific grid button
        def __init__(self, controller, x: int, y: int, state: bool = False):
            self.controller = controller
            self.x = x
            self.y = y
            self.state = state

        @staticmethod
        def get_xy_from_button_num(button_num):
            for column in APCMini.GridMapping:
                x = APCMini.GridMapping.index(column)
                if button_num in column:
                    return x, APCMini.GridMapping[x].index(button_num)
                else:
                    continue
            raise ValueError("GridButton not found!")

        def set_led(self, colour):
            """Sets this specific button's LED to be the colour given"""
            if isinstance(colour, int):
                if 0 <= colour <= 6:
                    self.controller.midi_out.send(
                        mido.Message("note_on", note=APCMini.GridMapping[self.x][self.y], velocity=colour))
                else:
                    raise ValueError("Grid colours can only be between 0 and 6")
            else:
                if colour in APCMini.GridColours:
                    self.controller.midi_out.send(
                        mido.Message("note_on", note=APCMini.GridMapping[self.x][self.y],
                                     velocity=APCMini.GridColours[colour]))
                else:
                    raise ValueError(
                        "The only valid colours for the grid are 'off', 'green', 'green_blinking', 'red', 'red_blinking', "
                        "'yellow', 'yellow_blinking'")

    class Fader:  # A single fader
        def __init__(self, controller, fader_id, value):
            self.controller = controller
            self.fader_id = fader_id
            self.value = value

        @staticmethod
        def get_fader_id_from_number(fader_num):
            return APCMini.FaderMapping.index(fader_num)

    class SideButtons:  # All the side buttons
        def __init__(self, controller):
            self.controller = controller

        def set_led(self, button_id, colour):
            """Sets an LED on the side buttons"""
            APCMini.SideButton(self.controller, button_id).set_led(colour)

    class SideButton:  # A specific side button
        def __init__(self, controller, button_id: int, state: bool = False):
            self.controller = controller
            self.button_id = button_id
            self.state = state

        @staticmethod
        def get_button_id_from_button_num(button_num):
            return APCMini.SideButtonMapping.index(button_num)

        def set_led(self, colour):
            """Sets this specific button's LED to be the colour given"""
            if isinstance(colour, int):
                if 0 <= colour <= 6:
                    self.controller.midi_out.send(
                        mido.Message("note_on", note=APCMini.SideButtonMapping[self.button_id], velocity=colour))
                else:
                    raise ValueError("Side Button colours can only be between 0 and 2")
            else:
                if colour in APCMini.SideButtonColours:
                    self.controller.midi_out.send(
                        mido.Message("note_on", note=APCMini.SideButtonMapping[self.button_id],
                                     velocity=APCMini.SideButtonColours[colour]))
                else:
                    raise ValueError(
                        "The only valid colours for the side buttons are 'on', 'off', 'green', 'blinking_green'")

    class LowerButtons:  # All the lower buttons
        def __init__(self, controller):
            self.controller = controller

        def set_led(self, button_id, colour):
            """Sets an LED on the lower buttons"""
            APCMini.LowerButton(self.controller, button_id).set_led(colour)

    class LowerButton:  # A specific side button
        def __init__(self, controller, button_id: int, state: bool = False):
            self.controller = controller
            self.button_id = button_id
            self.state = state

        @staticmethod
        def get_button_id_from_button_num(button_num):
            return APCMini.LowerButtonMapping.index(button_num)

        def set_led(self, colour):
            """Sets this specific button's LED to be the colour given"""
            if isinstance(colour, int):
                if 0 <= colour <= 6:
                    self.controller.midi_out.send(
                        mido.Message("note_on", note=APCMini.LowerButtonMapping[self.button_id], velocity=colour))
                else:
                    raise ValueError("Lower Button colours can only be between 0 and 2")
            else:
                if colour in APCMini.LowerButtonColours:
                    self.controller.midi_out.send(
                        mido.Message("note_on", note=APCMini.LowerButtonMapping[self.button_id],
                                     velocity=APCMini.LowerButtonColours[colour]))
                else:
                    raise ValueError(
                        "The only valid colours for the lower buttons are 'on', 'off', 'green', 'blinking_green'")

    class ShiftButton:  # The shift button
        def __init__(self, controller, state: bool = False):
            self.controller = controller
            self.state = state

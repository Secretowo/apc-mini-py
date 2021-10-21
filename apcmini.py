import mido

class ApcMini:
	activity = 0
	def __init__(self, midi_in=None, midi_out=None):
		self.midi_out = mido.open_output(midi_out)
		self.midi_in = mido.open_input(midi_in)
	def reset(self):
		for buttons in [range(0, 72), range(82, 90)]:
			for button in buttons:
				self.set(button, 0)
	def available_colors(self, button):
		if button <= 63:
			return {"off": 0, "green": 1, "green_blinking": 2, "red": 3, "red_blinking": 4, "yellow": 5, "yellow_blinking": 6}
		elif 64 <= button <= 71:
			return {"on": 1, "off": 0, "red": 1, "red_blinking": 2}
		elif 82 <= button <= 89:
			return {"on": 1, "off": 0, "green": 1, "green_blinking": 2}
		return {}
	def set(self, button, state):
		if type(state) == int:
			self.midi_out.send(mido.Message("note_on", note=button, velocity=state))
			self.activity += 1
			return
		elif state in (features := self.available_colors(button)):
			self.midi_out.send(mido.Message("note_on", note=button, velocity=features[state]))
			self.activity += 1
		else:
			raise ValueError(f"State '{state}' unknown or unsupported by button.")
		
	def pending_inputs(self):
		return self.midi_in.iter_pending()
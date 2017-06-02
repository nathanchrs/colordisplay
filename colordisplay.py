# Driver for Color Display Module
# Serial configuration: 8/N/1, baud rate 9600/19200 according to DIP switch (off = 9600)
# Data format: Modbus RTU

import minimalmodbus
import time

COLOR_RED = 256
COLOR_GREEN = 512
COLOR_BLUE = 1024
BLINK = 32768

COLOR_MAP = {
	'k': 0,		# Black
	'r': 256, 	# Red
	'g': 512,	# Green
	'y': 768,	# Yellow
	'b': 1024,	# Blue
	'm': 1280,	# Magenta
	'c': 1536,	# Cyan
	'w': 1792,	# White
}

LINE_WIDTH = 21

WATCHDOG_INTERVAL_REGISTER = 2
LINE_1_START_REGISTER = 10
LINE_2_START_REGISTER = 31

BAUD_RATE = 9600
DELAY_BETWEEN_OPERATIONS = 0.05

class ColorDisplay(minimalmodbus.Instrument):
	"""Instrument class for LED Color Display Module.

	Args:
		* device (str): device port name
		* device_address (int): device slave address (between 1 to 31)
	"""

	def __init__(self, device, device_address):
		minimalmodbus.Instrument.__init__(self, device, device_address)
		display.serial.baudrate = BAUD_RATE

	def get_watchdog_interval(self):
		"""Get watchdog timer interval in seconds. An interval of 1 indicates that the watchdog timer is disabled."""
		time.sleep(DELAY_BETWEEN_OPERATIONS)
		return self.read_register(WATCHDOG_INTERVAL_REGISTER)

	def set_watchdog_interval(self, seconds):
		"""Set watchdog timer interval (after the specified interval, the display will show the standby text).
		
		Args:
			* seconds (int): interval in seconds (1-65535). To disable watchdog timer, set interval to 1.
		"""	
		time.sleep(DELAY_BETWEEN_OPERATIONS)
		try:
			self.write_register(WATCHDOG_INTERVAL_REGISTER, seconds)
		except IOError:
			pass

	def set_text(self, text, color, line):
		"""Displays text on the display on a line (1 or 2) with the specified color."""

		line_text = list(text[:LINE_WIDTH].ljust(LINE_WIDTH, ' '))
		line_data = map(lambda c: ord(c) | color, line_text)

		start_register_address = LINE_1_START_REGISTER
		if line == 2:
			start_register_address = LINE_2_START_REGISTER

		time.sleep(DELAY_BETWEEN_OPERATIONS)
		try:
			self.write_registers(start_register_address, line_data)
		except IOError:
			pass

# Notes:
# - DELAY_BETWEEN_OPERATIONS must be set to a value greater than 0.05 seconds.
# - Still can't write to line 2 after writing to line 1?

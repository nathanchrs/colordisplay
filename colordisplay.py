# Driver for Color Display Module
# Serial configuration: 8/N/1
# Data format: Modbus RTU

import serial
import modbus_tk
import modbus_tk.defines as operations
from modbus_tk import modbus_rtu
from modbus_tk.modbus import ModbusError

COLOR_MAP = {
	'r': 256, 	# Red
	'g': 512,	# Green
	'y': 768,	# Yellow
	'b': 1024,	# Blue
	'm': 1280,	# Magenta
	'c': 1536,	# Cyan
	'w': 1792	# White
}

BLINK = 32768
LINE_WIDTH = 21

WATCHDOG_INTERVAL_REGISTER = 2
DISPLAY_START_REGISTER = 10

DEVICE_TIMEOUT = 1.0


class ColorDisplay:
	"""Instrument class for LED Color Display Module.

	Args:
		* device (str): device port name
		* device_address (int): device slave address (between 1 to 31)
	"""

	def __init__(self, device, device_address, baud_rate):
		self.device = modbus_rtu.RtuMaster(
			serial.Serial(port=device, baudrate=baud_rate, bytesize=8, parity='N', stopbits=1, xonxoff=0)
		)
		self.device.set_timeout(DEVICE_TIMEOUT)
		self.device.set_verbose(True)
		self.device_address = device_address

	
	def show_page(self, page):

		line_1_data = convert_line_to_data(page['first_line_text'], page['first_line_color'])
		line_2_data = convert_line_to_data(page['second_line_text'], page['second_line_color'])
		line_data = line_1_data + line_2_data

		try:
			self.device.execute(
				self.device_address, operations.WRITE_MULTIPLE_REGISTERS, DISPLAY_START_REGISTER, output_value = line_data
			)
		except ModbusError as ex:
			print 'Failed to show page:'
			print page
			print ex


def convert_line_to_data(text, color):
	"""Helper function to convert text and color strings to Modbus data.
	Text and color will be truncated according to LINE_WIDTH, color will be converted according to color map.
	Uppercase letter for color will set the character to blink.
	"""

	line_text = list(text[:LINE_WIDTH].ljust(LINE_WIDTH, ' '))
	line_color = list(color[:LINE_WIDTH].ljust(LINE_WIDTH, 'k'))

	line_data = []
	for i in range(0, len(line_text)):
		char_color = COLOR_MAP.get(line_color[i].lower(), 0);
		if line_color[i].isupper():
			char_color = char_color | BLINK
		line_data.append(ord(line_text[i]) | char_color)

	return line_data
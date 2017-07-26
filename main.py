#!/bin/env python

import os
import threading
import time
from serial.serialutil import SerialException

import colordisplay
from variables import *
import config_io


# Global variables 
pages = []
previous_display_file_last_modified = None
previous_display_interval_file_last_modified = None
display_interval = 5


def error_page(message = ''):
	"""Returns an error page with the specified message."""
	return {
		'first_line_text': '>ERROR',
		'first_line_color': 'Wrrrrrr',
		'second_line_text': message,
		'second_line_color': 'rrrrrrrrrrrrrrrrrrrrr'
	}


def display_file_check_thread():
	"""Thread which updates pages if the display or display interval file is modified."""

	global pages
	global display_interval
	global previous_display_file_last_modified
	global previous_display_interval_file_last_modified

	while True:

		# Check display file
		display_file_last_modified = None
		try:
			display_file_last_modified = os.stat(DISPLAY_FILE_PATH).st_mtime
		except:
			print 'Display file not found or not accessible.'
			pages = []

		if display_file_last_modified != None:
			if previous_display_file_last_modified != display_file_last_modified:
				if previous_display_file_last_modified == None:
					print 'Loading display file...'
				else:
					print 'Display file modified, reloading...'
				pages = config_io.read_from_display_file(DISPLAY_FILE_PATH)
				previous_display_file_last_modified = display_file_last_modified

		# Check display interval file
		display_interval_file_last_modified = None
		try:
			display_interval_file_last_modified = os.stat(DISPLAY_INTERVAL_FILE_PATH).st_mtime
		except:
			print 'Display interval file not found or not accessible.'
			display_interval = None

		if display_interval_file_last_modified != None:
			if previous_display_interval_file_last_modified != display_interval_file_last_modified:
				if previous_display_interval_file_last_modified == None:
					print 'Loading display interval file...'
				else:
					print 'Display interval file modified, reloading...'
				display_interval = config_io.read_from_display_interval_file(DISPLAY_INTERVAL_FILE_PATH)
				previous_display_interval_file_last_modified = display_interval_file_last_modified

		time.sleep(FILE_CHECK_INTERVAL)


# Main program
if __name__ == "__main__":
	
	# Initialize display
	print 'Initializing display device...'
	try:
		display = colordisplay.ColorDisplay(DEVICE, DEVICE_ADDRESS, DEVICE_BAUD_RATE);
	except SerialException:
		print 'Failed to connect to serial device', DEVICE
		exit(1)

	# Start display file checking thread
	print 'Starting display file check thread...'
	threading.Thread(target = display_file_check_thread).start()
	time.sleep(0.5) # Wait a little to let file check threads to start before continuing.

	# Display each page in a loop
	print 'Displaying pages...'
	current_page_index = 0
	while True:
		if pages == None:
			display.show_page(error_page('Invalid display text'))
		elif len(pages) == 0:
			display.show_page(error_page('No display text'))
		elif display_interval == None:
			display.show_page(error_page('Invalid interval'))
		else:
			page_count = len(pages)
			if current_page_index < page_count and page_count > 0:
				display.show_page(pages[current_page_index])
				current_page_index = (current_page_index + 1) % page_count
			else:
				current_page_index = 0

		if display_interval == None:
			time.sleep(5)
		else:
			time.sleep(display_interval)

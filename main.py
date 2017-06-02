#!/bin/env python

import os
import threading
import time
from serial.serialutil import SerialException

import colordisplay
from config import *


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


def read_from_display_file(display_file_path):
	"""Reads and returns a list of pages from the display file."""

	# Read all non-empty lines from file
	lines = []
	try:
		with open(display_file_path, 'r') as fin:
			lines = [line for line in fin.readlines() if line.strip() != '']
	except:
		print 'Failed to read from display file.'
		return None

	# Invalid file, wrong number of non-empty lines
	if len(lines) % 4 != 0:
		print 'Invalid display file format: wrong number of non-empty lines.'
		return None

	# Convert lines to list of pages
	pages = []
	for i in range(0, len(lines), 4):
		page = {
			'first_line_text': lines[i],
			'first_line_color': lines[i+1],
			'second_line_text': lines[i+2],
			'second_line_color': lines[i+3]
		}
		pages.append(page)

	return pages


def read_from_display_interval_file(display_interval_file_path):
	"""Reads and returns an integer value from the display interval file."""

	try:
		with open(display_interval_file_path, 'r') as fin:
			lines = [line for line in fin.readlines() if line.strip() != '']
		disp_interval = int(lines[0].strip())

		if disp_interval < 1:
			print 'Invalid display interval value.'
			return None

		return disp_interval

	except:
		print 'Invalid display interval file.'
		return None


def display_file_check_thread():
	"""Thread which updates pages if the display or display interval file is modified."""

	global pages
	global display_interval
	global previous_display_file_last_modified
	global previous_display_interval_file_last_modified

	while True:

		# Check display file
		display_file_last_modified = os.stat(DISPLAY_FILE_PATH).st_mtime
		if previous_display_file_last_modified != display_file_last_modified:
			if previous_display_file_last_modified == None:
				print 'Loading display file...'
			else:
				print 'Display file modified, reloading...'
			pages = read_from_display_file(DISPLAY_FILE_PATH)
			previous_display_file_last_modified = display_file_last_modified

		# Check display interval file
		display_interval_file_last_modified = os.stat(DISPLAY_INTERVAL_FILE_PATH).st_mtime
		if previous_display_interval_file_last_modified != display_interval_file_last_modified:
			if previous_display_interval_file_last_modified == None:
				print 'Loading display interval file...'
			else:
				print 'Display interval file modified, reloading...'
			display_interval = read_from_display_interval_file(DISPLAY_INTERVAL_FILE_PATH)
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
	time.sleep(0.5)

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
			time.sleep(1)
		else:
			time.sleep(display_interval)

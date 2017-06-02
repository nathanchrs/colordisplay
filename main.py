#!/bin/env python

import os
import threading
import time
from serial.serialutil import SerialException
import colordisplay
from config import *


# Global variables 
pages = []
previous_display_file_last_modified_time = None


# Main program
if __name__ == "__main__":
	
	# Initialize display
	try:
		display = colordisplay.ColorDisplay(DEVICE, DEVICE_ADDRESS);
	except SerialException:
		print 'Failed to connect to serial device', DEVICE
		exit(1)

	# Start display file checking thread
	threading.Thread(target = display_file_check_thread).start()

	# Display each page in a loop
	current_page_index = 0
	while True:
		if current_page_index < len(pages):
			display.show_page(page[current_page_index])
			time.sleep(DISPLAY_INTERVAL)
			current_page_index = current_page_index + 1
		else:
			current_page_index = 0


def display_file_check_thread():
	while True:
		if is_file_modified(previous_display_file_last_modified_time, DISPLAY_FILE_PATH):
			pages = read_from_display_file(DISPLAY_FILE_PATH)
		time.sleep(FILE_CHECK_INTERVAL)
		yield


def is_file_modified(previous_last_modified_time, file_path):
	last_modified_time = os.stat(file_path).st_mtime
	return previous_last_modified_time != last_modified_time


def read_from_display_file(display_file_path):

	# Read all non-empty lines from file, then remove leading and trailing whitespace
	with open(dsplay_file_path, 'r') as fin:
		lines = [line.strip() for line in fin.readlines() if line.strip() != '']

	# Invalid file, wrong number of non-empty lines
	if len(lines) % 4 != 0:
		return []

	# Convert lines to list of pages
	pages = []
	for i in range(0, len(lines), 4):
		page = {
			'first_line_chars': lines[i],
			'first_line_colors': lines[i+1],
			'second_line_chars': lines[i+2],
			'second_line_colors': lines[i+3]
		}
		pages.append(page)

	return pages

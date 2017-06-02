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

def save_display_interval_to_file(display_interval_file_path, display_interval):
	"""Saves the display interval value to file."""
	with open(display_interval_file_path, 'w') as fout:
		fout.write(display_interval)

#!/bin/env python

from flask import Flask, request, render_template, redirect, url_for

import config_io
from variables import DISPLAY_FILE_PATH, DISPLAY_INTERVAL_FILE_PATH

app = Flask(__name__)


@app.route('/')
def show_config_page():
	pages = config_io.read_from_display_file(DISPLAY_FILE_PATH)
	display_interval = config_io.read_from_display_interval_file(DISPLAY_INTERVAL_FILE_PATH)

	# TODO: display pages and interval's existing values in form
	# TODO: js-based array input for pages
	return render_template('configpage.html', pages=pages, display_interval=display_interval)


@app.route('/display', methods=['POST'])
def save_display():
	# TODO: implement save display text and colors
	return redirect('/')


@app.route('/interval', methods=['POST'])
def save_display_interval():
	config_io.save_display_interval_to_file(DISPLAY_INTERVAL_FILE_PATH, request.form['display_interval'])
	return redirect(url_for('show_config_page'))

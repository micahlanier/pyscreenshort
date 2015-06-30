#!/usr/bin/env python

##### Setup

### Libraries

import argparse
import logging
import math
import os
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
import re
import sys

### System Settings

# Default font paths for Mac OS X.
# Order of list will be searchable order.
font_dirs = ['/System/Library/Fonts/','/Library/Fonts/','~/Library/Fonts/']

### Visual Settings

# Rendering scale.
# PIL fonts are rough, so we want to render the image larger and resize with anti-aliasing.
render_scale = 4

# Default dimensions.
default_min_height = 240
default_width = 600
default_padding = 20

# Default colors if received options are unparseable.
default_color_bg = 'white'
default_color_text = 'black'

# Default fonts and related options.
default_font_major = 'Hoefler Text'
default_font_minor = 'HelveticaNeue'
default_font_size_major = 24
default_font_size_minor = 16
default_font_spacing_major = 1
default_font_spacing_minor = 0

##### Functions

def process_text(text, font, width_limit):
	"""Reformat text as a set of appropriate-length lines given a font and width limit. Return a list of strings (one line per entry).

	Keyword arguments:
		text: raw text to format.
		font: PIL font to use for formatting.
		width_limit: width limit of text area in pixels.
	"""
	# Tokenize each line.
	tokens = [re.sub(ur'\s+',' ',line.strip()).split(' ') for line in text.strip().split('\n')]
	# Create a container and traverse lines.
	tokens_processed = []
	for l, line in enumerate(tokens):
		# Always append the first token. This handles empty lines, too-long tokens.
		current_line = [line[0]]
		# Traverse all tokens on this line.
		for token in line[1:]:
			# Test the new line.
			proposal = ' '.join(current_line+[token])
			if font.getsize(proposal)[0] < width_limit:
				# If the new token does not make the line too long, append it.
				current_line.append(token)
			else:
				# Otherwise, start a new line.
				tokens_processed.append(current_line)
				current_line = [token]
		# At this point, we have finished processing a line. Add what remains to the full line list.
		tokens_processed.append(current_line)
	# Finally, bring it all together and return.
	return [' '.join(tokens) for tokens in tokens_processed]

def find_font_by_name(path, name):
	"""Find a font at a given path and return the whole path or None (if not found).

	Keyword arguments:
		path: directory to search.
		name: font name based on filename without extension.
	"""
	# Validate path.
	path = os.path.expanduser(path)
	if not os.path.isdir(path): return None
	# Traverse.
	found_fonts = [f for f in os.listdir(path) if os.path.splitext(f)[0] == name]
	return (os.path.join(path,found_fonts[0]) if found_fonts else None)

def draw_text(image, lines, x, y, spacing, font, color):
	"""Draw lines of text on a given image.

	Keyword arguments:
		image: PIL.Image on which to draw text.
		lines: list of strings (each one line).
		x: horizontal location to begin drawing text.
		y: vertical location to begin drawing text.
		spacing: spacing between lines in pixels.
		font: PIL ImageFont object.
		color: PIL.ImageColor name (e.g., 'red', 'darkgreen', '#ffffff').
	"""
	# Draw the main text.
	draw = ImageDraw.Draw(image)
	# Keep track of line offset from top.
	line_offset = y
	# Traverse all lines.
	for line in lines:
		# Draw text.
		draw.text((x,line_offset), line, font=font, fill=color)
		# Update offset.
		line_offset += sum(font.getmetrics()) + spacing

def validate_color(color,default,color_type):
	"""Validate a color against known PIL values. Return the validated color if valid; otherwise return a default.

	Keyword arguments:
		color: color to test.
		default: default color string value if color is invalid.
		color_type: string name for color type, used for alerting users of defaults.
	"""
	# Use exception handling. If a given color throws an error, we may return false.
	try:
		c = ImageColor.getcolor(color,'RGB')
		return color
	except ValueError as e:
		logging.warning('"%s" is not a valid color specifier. Defaulting to "%s" for %s color.',color,default,color_type)
		return default

##### Execution

def screenshort(
	main_text,
	secondary_text=None,
	width=default_width,
	min_height=default_min_height,
	padding=default_padding,
	bg_color=default_color_bg,
	text_color=default_color_text,
	major_font_name=default_font_major,
	major_font_size=default_font_size_major,
	major_font_spacing=default_font_spacing_major,
	major_text_color=None,
	minor_font_name=default_font_minor,
	minor_font_size=default_font_size_minor,
	minor_font_spacing=default_font_spacing_minor,
	minor_text_color=None,
	output=None
):
	"""Generate a screenshort and save to the specified path.""""

	### Input Validation

	# Determine if we're using minor text or not.
	use_minor_text = secondary_text not in {'',None}

	# Validate size.
	if width < padding*2:
		logging.error('Image width must be larger than 2*padding.')
		sys.exit(1)
	elif width < 200:
		logging.warning('Image width %d will likely produce a very cramped image.',width)
	min_height = max(0,min_height)
	padding = max(0,padding)

	# Validate colors.
	color_bg   = validate_color(bg_color,default_color_bg,'background')
	color_text = validate_color(text_color,default_color_text,'text')
	# Intelligently select colors for each type of text.
	color_text_major = color_text if major_text_color is None else validate_color(major_text_color,'main text',color_text)
	color_text_minor = color_text if minor_text_color is None else validate_color(minor_text_color,'secondary text',color_text)

	# Validate text/font settings.

	# TODO

	### Process Settings

	# This section sets up variables that we will actually use in the rendering process.

	# Parse text as UTF-8.
	text_major = main_text.decode('utf-8')
	if use_minor_text: text_minor = secondary_text.decode('utf-8')

	# Get rendering width.
	render_width = width * render_scale
	# Scale-specific padding and text margins.
	render_padding = padding * render_scale
	font_spacing_render_major = padding * major_font_spacing
	font_spacing_render_minor = padding * minor_font_spacing
	# Determine how much space the text has.
	render_text_width = render_width - render_padding*2
	# Determine minimum render height.
	render_height_min = min_height*render_scale

	# Get fonts.
	font_path_major = None
	font_path_minor = None
	# Traverse font directories.
	for font_dir in reversed(font_dirs):
		# Get candidates for fonts.
		font_candidate_major = find_font_by_name(font_dir, major_font_name)
		font_path_major = font_candidate_major if font_candidate_major else font_path_major
		font_candidate_minor = find_font_by_name(font_dir, minor_font_name)
		font_path_minor = font_candidate_minor if font_candidate_minor else font_path_minor
	# Validate fonts.
	if not font_path_major:
		logging.error('No valid main text font found.')
		sys.exit(1)
	if use_minor_text and not font_path_major:
		logging.error('No valid secondary text font found.')
		sys.exit(1)

	# Turn fonts into actual objects.
	font_major = ImageFont.truetype(font_path_major, major_font_size*render_scale, encoding='unic')
	font_minor = ImageFont.truetype(font_path_minor, minor_font_size*render_scale, encoding='unic')
	# Get their line heights for later use as well.
	line_height_major = sum(font_major.getmetrics())
	line_height_minor = sum(font_minor.getmetrics())

	# Get height of each text element
	text_lines_major = process_text(text_major, font_major, render_text_width)
	if use_minor_text:
		# If there is secondary text, process it.
		text_lines_minor = process_text(text_minor, font_minor, render_text_width)
		# Also handle spacing in between major/minor text.
		intratext_spacing = line_height_major
	else:
		# No minor text height or buffer after major text if there is no minor text.
		line_height_minor = 0
		intratext_spacing = 0

	# Determine height. Calculate what it should be.
	text_height_major = len(text_lines_major)*line_height_major + (len(text_lines_major)-1)*font_spacing_render_major
	text_height_minor = len(text_lines_minor)*line_height_minor + (len(text_lines_minor)-1)*font_spacing_render_minor if use_minor_text else 0
	render_height = (text_height_major+intratext_spacing+text_height_minor+render_padding*2)
	height = render_height/render_scale
	# Location for minor text to start.
	text_minor_y = max(render_height,render_height_min)-(render_padding+text_height_minor)
	# Alter height if the determined height is below minimum.
	if render_height < render_height_min:
		# If it's too small, adjust.
		render_height = render_height_min
		# Also make sure the main text starts middle-aligned.
		text_major_y = (text_minor_y+render_padding)/2 - text_height_major/2
	else:
		text_major_y = render_padding
	# Determine final unscaled height.
	height = render_height/render_scale

	### Image Composition

	# Now we're ready to compose the image. Start by creating it.
	img = Image.new('RGBA', (render_width,render_height), color_bg)

	# Draw text.
	draw_text(img, text_lines_major, render_padding, text_major_y, font_spacing_render_major, font_major, color_text_major)
	if use_minor_text:
		draw_text(img, text_lines_minor, render_padding, text_minor_y, font_spacing_render_minor, font_minor, color_text_minor)

	# Resize back down to intended size.
	# Use anti-aliasing. Inspiration: http://stackoverflow.com/questions/5414639/python-imaging-library-text-rendering
	img_resized = img.resize((width,height), Image.ANTIALIAS)

	# Save/show it.
	if output is None:
		img_resized.show()
	else:
		img_resized.save(output)

##### Standalone Execution

def main():
	"""Parse input arguments and pass to screenshort()."""
	# Set up argument parser.
	parser = argparse.ArgumentParser(description='Generate a "screenshort" image.')
	# Text elements.
	parser.add_argument('main_text',type=str,help='main image text')
	parser.add_argument('secondary_text',nargs='?',type=str,help='secondary image text (optional)')
	# Image size.
	group_size = parser.add_argument_group('Image Size')
	group_size.add_argument('--min_height',metavar='PIXELS',type=int,default=default_min_height,help='minimum height in pixels (default: %d)'%default_min_height)
	group_size.add_argument('--width',metavar='PIXELS',type=int,default=default_width,help='width in pixels (default: %d)'%default_width)
	group_size.add_argument('--padding',metavar='PIXELS',type=int,default=default_padding,help='padding in pixels around the outside of the image (default: %d)'%default_padding)
	# Output.
	group_output = parser.add_argument_group('File Output')
	group_output.add_argument('--output',metavar='LOCATION',type=str,default=None,help='output destination file, including extension. if omitted, a BMP will be created and shown via xv')
	# Colors.
	group_color = parser.add_argument_group('Colors')
	group_color.add_argument('--bg_color',metavar='COLOR',dest='bg_color',type=str,default=default_color_bg,help='background color, a hexadecimal string or common color name (default: %s)'%default_color_bg)
	group_color.add_argument('--text_color',metavar='COLOR',dest='text_color',type=str,default=default_color_text,help='text color, a hexadecimal string or common color name (default: %s)'%default_color_text)
	group_color.add_argument('--main_text_color',metavar='COLOR',dest='major_text_color',type=str,default=None,help='main string text color (defaults to --text_color value)')
	group_color.add_argument('--secondary_text_color',metavar='COLOR',dest='minor_text_color',type=str,default=None,help='secondary string text color (defaults to --text_color value)')
	# Fonts.
	group_fonts = parser.add_argument_group('Fonts')
	group_fonts.add_argument('--main_font_name',metavar='FONT',dest='major_font_name',type=str,default=default_font_major,help='font name for main text, based on font filename with no extension (default: %s)'%default_font_major)
	group_fonts.add_argument('--secondary_font_name',metavar='FONT',dest='minor_font_name',type=str,default=default_font_minor,help='font name for secondary text, based on font filename with no extension (default: %s)'%default_font_minor)
	group_fonts.add_argument('--main_font_size',metavar='POINTS',dest='major_font_size',type=int,default=default_font_size_major,help='font size for main text in points (default: %d)'%default_font_size_major)
	group_fonts.add_argument('--secondary_font_size',metavar='POINTS',dest='minor_font_size',type=int,default=default_font_size_minor,help='font size for secondary text in points (default: %d)'%default_font_size_minor)
	group_fonts.add_argument('--main_font_spacing',metavar='PIXELS',dest='major_font_spacing',type=int,default=default_font_spacing_major,help='inter-line spacing for main text (default: %d)'%default_font_spacing_major)
	group_fonts.add_argument('--secondary_font_spacing',metavar='PIXELS',dest='minor_font_spacing',type=int,default=default_font_spacing_minor,help='inter-line spacing for secondary text (default: %d)'%default_font_spacing_minor)
	# Parse arguments.
	args = parser.parse_args()
	# Simply pass params to screenshort() method.
	screenshort(**vars(args))

if __name__ == '__main__':
	main()

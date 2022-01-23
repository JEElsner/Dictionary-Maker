# Author: ???
# 2018-07-03
#
# Update from the future: I doubt I wrote this code. It has docstrings when I probably didn't know
# what docstrings were. I don't know who wrote the code, or where I got it from. Don't attribute
# this work to me.
#
# A set of methods to manipulate and test XML files
#
# Dependencies
# ------------
# keyboard


import keyboard  # Necessary to receive user input


# Reduced File Size:
new_file_size = 1048576  # 1 MiB (in bytes)


def create_small(old_file, new_file, size_addition=0, append=''):
	"""
	Create a small file that can be quickly read and parsed
	:param old_file: The file to be copied smaller
	:param new_file: The location to which the reduced file will be put
	:param size_addition: How many bytes to read in excess of new_file_size
	:param append: What to append at the end of the file, used to resolve XML tags (e.g. append: </doc>)
	"""
	# Open the original file
	# UTF-8 is necessary because some bytes are non-ASCII, such as chinese characters
	in_file = open(old_file, 'r', encoding='utf-8')
	# Open the new file
	# UTF-8 is necessary because some bytes are non-ASCII, such as chinese characters
	out_file = open(new_file, 'w', encoding='utf-8')

	# Write the subsection of the old file to the new one
	out_file.write(in_file.read(new_file_size + size_addition))
	# Write out the appendage specified in the argument
	out_file.write(append)


# This probably should be split into two functions because of its varied functionality, but I'm lazy, so ¯\_(ツ)_/¯
# Oh, and props to python for making its default encoding to UTF-8, so I can put in that shrug face
def print_reader(file, more=False, size_addition=0):
	"""
	Prints new_file_size + size_addition bytes to the console. If the <code>more</code> is true, accept more lines by
	user input
	:param file: The file to read
	:param more: Whether to grab more data according to user input or not
	:param size_addition: How many bytes to read in excess of new_file_size
	:return the excess bytes printed after new_file_size
	"""

	if more:  # Print out user instructions if necessary
		print(new_file_size, ' bytes will be printed to the console. Afterward, press SPACE to print more lines, and Q ',
								'to stop printing lines and print how many bytes were printed in excess of ',
								new_file_size, '.\n(Press ENTER to continue)')
		input()  # Wait for the user to read the message

	# Open the specified file
	# UTF-8 is necessary because some bytes are non-ASCII, such as chinese characters
	in_file = open(file, 'r', encoding='utf-8')

	# Iterate through new_file_size + size_addition bytes
	for i in range(0, new_file_size + size_addition):
		# Print the byte to the console (without a newline because the last byte of each line will be a newline)
		print(in_file.read(1), end='')

	if not more:  # If more bytes won't be accepted, return now
		return 0

	counter = 0  # A counter of how many extra bytes are printed
	while True:

		while not keyboard.is_pressed(' '):  # Wait for the space key to be pressed
			printed = False  # reset the printed flag to prevent multiple lines from printing per 'SPACE' press

			if keyboard.is_pressed('q'):  # See if the 'q' is pressed to quit printing extra lines
				print(counter)  # Print the number of excess bytes written
				return counter  # Return the number of excess bytes

		if not printed:  # Determine if a line has already been printed when the space key has been pressed
			line = in_file.readline()  # Read the line from file
			print(line, end='')  # Write the line to console

			counter += len(line)  # Add the number of bytes in the line to the counter

			printed = True  # Set a flag preventing multiple lines from printing per 'SPACE' press


def navigator(file):
	"""
	Prompt the user for a line number of the given file, then print off that line
	:param file: The XML file to navigate
	:return: None
	"""
	print('Enter a line number to print that line, enter \'q\' to quit:')  # Give the user directions

	# Open the specified file
	# UTF-8 is necessary because some bytes are non-ASCII, such as chinese characters
	in_file = open(file, encoding='utf-8')

	while True:  # Run until the user is done navigating
		line_number = input('>')  # Take the line number from the user

		if line_number.lower().__contains__('q'):  # Check if the user wants to quit, and then quit
			return

		for i, line in enumerate(in_file):  # Iterate through each line of the file
			try:
				if i == int(line_number) - 1:  # Check if the iterated line is the line the user wants printed
					print(line, end='')  # Print the line (without a newline because the last byte of each line will be a newline)
					break  # Stop iterating through lines because the desired line has been found
			except ValueError:  # Prevent dumb users from crashing the program when they put 'lfkasdfoyh' instead of '3'
				print('Invalid line number: ' + line_number)
				break

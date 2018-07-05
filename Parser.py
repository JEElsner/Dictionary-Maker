# Author: Jonathan Elsner
# 2018-07-03
#
# A fairly lightweight script to sort english words in a Wiktionary dump into different files according to the letters
# they contain.
#
# I'm working on a program to learn the Dvorak keyboard layout that adapts to the mistakes you make. For this project
# I need lists of words that can be typed with only specific letters, (e.g. letters in the home row)
#
# Wikipedia Dump Used
# -------------------
# 'Extracted page abstracts for Yahoo' 2018-02
# 2018-02 Dump Overview: https://dumps.wikimedia.org/enwiktionary/20180220/
# Specific Dump File Used: https://dumps.wikimedia.org/enwiktionary/20180220/enwiktionary-20180220-abstract.xml.gz

import re  # Regex capabilities
import datetime  # Date stamp capabilities
import os  # File path joining capabilities
import sys  # Used to get the file location of the script

import FileUtility as FU  # A simple python file for manipulation and testing of XML files


print('Using path: ' + sys.path[0])  # Print the path of script

# The original, large file:
original_file = os.path.join(sys.path[0], 'enwiktionary-20180220-abstract.xml')

# A smaller part of the original file:
small_file = os.path.join(sys.path[0], 'small.xml')

# Directory to put the generated dictionaries in: (must exist)
dictionary_dir = sys.path[0]

# Each dictionary file
home8_dict = open(os.path.join(dictionary_dir, 'home8.txt'), 'w')
home10_dict = open(os.path.join(dictionary_dir, 'home10.txt'), 'w')
c_set_dict = open(os.path.join(dictionary_dir, 'c_set.txt'), 'w')
b_set_dict = open(os.path.join(dictionary_dir, 'b_set.txt'), 'w')
entire_dict = open(os.path.join(dictionary_dir, 'entire_alphabet.txt'), 'w')

# Log file
log = open(dictionary_dir + 'log.txt', 'w')


# Create regex objects to sort for words containing only letters for each category
# Pattern: '\\b[#letters#]+\\b(?!\\w)'

home8 = re.compile('\\b[aoeuhtns]+\\b(?!\\w)')  # 8 Home Row keys, the keys your fingers rest on
home10 = re.compile('\\b[aoeuidhtns]+\\b(?!\\w)')  # 10 Home Row keys, the previous category + i and d
c_set = re.compile('\\b[aoeuidhtnscfklmprv]+\\b(?!\\w)')  # Home Row + c, f, k, l, m, p, r, and v
b_set = re.compile('\\b[aoeuidhtnsbgjqwxyz]+\\b(?!\\w)')  # Home Row + b, g, j, q, w, x, y, z

alphabets = re.compile('\\b[a-z]+\\b(?!.)')  # Regex to ensure the entry is one word, with no special characters


def header(file, title, letters):
	"""
	Write header descriptions to specified dictionary
	:param file: The dictionary file to which to write the header
	:param title: The title of the dictionary
	:param letters: The letters included in the words contained in the dictionary. Use a string, for example: 'A, B, C'
	or 'Letters A-Z'
	"""

	file.write(' # ' + title + ' Dictionary\n')
	file.write(' # Contains letters:' + letters + '\n')
	file.write(' # Generator created by: Jonathan Elsner')
	file.write(' # Words compiled from 2018-02 \'Extracted page abstracts for Yahoo\' Wiktionary dump: '
			   'https://dumps.wikimedia.org/enwiktionary/20180220/')
	file.write(' # Specific File: https://dumps.wikimedia.org/enwiktionary/20180220/enwiktionary-20180220-abstract.xml.gz')
	file.write(' # Copyright: CC BY-SA 3.0 ---> https://creativecommons.org/licenses/by-sa/3.0/')
	file.write(' # Generated: ' + str(datetime.datetime.now()) + '\n\n')


# Create headers for each dictionary
header(home8_dict, 'Home 8', 'A, O, E, U, H, T, N, S')
header(home10_dict, 'Home 10', 'A, O, E, U, I, D, H, T, N, S')
header(c_set_dict, 'C Set Dictionary', 'A, O, E, U, I, D, H, T, N, S, C, F, K, L, M, P, R, V')
header(b_set_dict, 'B Set Dictionary', 'A, O, E, U, I, D, H, T, N, S, B, G, J, Q, W, X, Y, Z')
header(entire_dict, 'All Letter', 'Entire Roman Alphabet')


# Create a smaller file from the large one for testing purposes
#
# The specified 'size_addition' and 'append' are necessary to make the file valid XML.
# 'size_addition' takes that many more bytes than the default 'FU.new_file_size' from the old file,
# 	writing them to the new file to complete an XML tag.
# 'append' appends the specified text to the end of the file, again to complete an XML tag
#
# FU.create_small(original_file, small_file, size_addition=155, append='</feed>')

# Print part of the file to the console
# FU.print_reader(original_file, size_addition=155, more=False)

# Counters to keep track of different metrics of the wiki dump
current_entry = 0
english_entries = 0
valid_words = 0


# Open the file to be read and parsed
# UTF-8 is necessary because some bytes are non-ASCII, such as chinese characters
in_file = open(original_file, 'r', encoding='utf-8')


begin_time = datetime.datetime.now()  # Record the beginning time of the parse

# Print and log feedback info
#
# There's probably a nice little API to handle logging, but I want this program to be a quick,
# lightweight solution, so this is the result
print('[' + str(begin_time) + ']: Beginning Parse...')
log.write('[' + str(begin_time) + ']: Beginning Parse...\n')


# Iterate through each line of the dump file
for line in in_file:
	if line.startswith('<title>'):  # Find Wiktionary page titles
		# take the entry (all element[0] = <title> tags begin with: '<title>Wiktionary: ' and end with: '</title>\n'
		entry = line[19:-9].lower()

		next(in_file)  # Skip the next line before the <abstract> tag (it's a <url> tag, which we don't need)
		abstract = in_file.readline()  # Read the line containing the language

		if abstract.__contains__('English'):  # Check if the page is an english entry
			english_entries += 1  # Increment the number of english entry found

			# Eliminate entries that contain spaces or non-alphabets
			if not alphabets.match(entry):
				continue

			valid_words += 1  # Increment the number of valid words found

			# Add the word to the correct dictionaries:

			if home8.match(entry):
				home8_dict.write(entry + '\n')

			elif home10.match(entry):
				home10_dict.write(entry + '\n')

			elif c_set.match(entry):
				c_set_dict.write(entry + '\n')

			elif b_set.match(entry):
				b_set_dict.write(entry + '\n')

			else:
				entire_dict.write(entry + '\n')

	current_entry += 1  # Increment a counter of all entries processed
	if current_entry % 1000000 == 0:  # Print out and log a message every 1 mil entries
		print(
			'[' + str(datetime.datetime.now()) + ']: ' + str(current_entry / 1000000) + ' million entries complete')
		log.write('[' + str(datetime.datetime.now()) + ']: ' + str(current_entry / 1000000) +
				  ' million elements complete\n')

# Print a final message summarizing the entries processed
print('[' + str(datetime.datetime.now()) + ']: ', current_entry, ' entries processed, ', english_entries,
	  ' were english, and ', valid_words, ' were valid words.')
log.write('[' + str(datetime.datetime.now()) + ']: ' + str(current_entry) + ' entries processed, ' +
		  str(english_entries) + ' were english, and ' + str(valid_words) + ' were valid words.\n')

print('Took: ' + str(datetime.datetime.now() - begin_time))
log.write('Took: ' + str(datetime.datetime.now() - begin_time))

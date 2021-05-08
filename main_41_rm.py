# Praktiskais darbs 4.1
# Raits Misiņš, e-IT2

# 4.1. Exploring e-mails received – handling words using lists:
# Write a program to read through the file mbox-short.txt and
# when you find line that starts with "From", you will
# split the line into words using the split function.
# We are interested in who sent the message which is the second word on the From line.
# From stephen.marquard@uct.ac.za Sat Jan 5 09:14:16 2008
# You will parse the From line and print out the second word for each From line and
# then you will also count the number of From (i.e. but not From:) lines
# and print out a count at the end. This is a sample good output with a few lines removed (see below).
# EXAMPLE:
# $ python via_counting_words.py
# Enter a file name: mbox-short.txt
# stephen.marquard@uct.ac.za
# louis@media.berkeley.edu
# zqian@umich.edu
# [...some output removed...]
# ray@media.berkeley.edu
# cwen@iupui.edu
# cwen@iupui.edu
# cwen@iupui.edu
# There were 27 lines in the file with From as the first word

import os
import re

FROM_TAG = "From "
WRONG_FROM = "From:"
EMAIL_SEPARATOR = "@"
#
# primitive e-mail regex used below will give a limited precision, but it should be enough for most cases
# Complete regexes for e-mail address validation are hundreds of characters long.
PRIMITIVE_EMAIL_REGEX = "\S+@\S+\.\S+"


def is_email_address(string_to_check):
    #
    # function is_email_address returns True only if the parameter string is an e-mail address
    # NB, this is function has limited precision, as a very rudimentary regex is used
    #
    result = re.match(PRIMITIVE_EMAIL_REGEX, string_to_check)

    return result


# mbox_file_name = input('Enter file name: ')
os.chdir(os.path.dirname(__file__))
mbox_file_name = 'mbox-short.txt'

try:
    mbox_file = open(mbox_file_name)
except OSError:
    print('*** ERROR: cannot open mailbox file ', mbox_file_name)
    quit(1)

from_counter = 0

for row in mbox_file:
    if row.startswith(FROM_TAG):    # since FROM_TAG includes space ('From ') there is no need
                                    # to check if the row starts with 'From:' --> "and not row.startswith(WRONG_FROM)"
        from_counter = from_counter + 1     # since requirement is count just lines starting with 'From '
        words_in_row = row.split()
        if is_email_address(words_in_row[1]):
            # check if the second word in a row is an e-mail address
            # it is possible that a random line in the mailbox just starts with 'From ', but is not
            # followed by an e-mail address
            print(words_in_row[1])
mbox_file.close()
print(from_counter)

# Praktiskais darbs 4.3
# Raits Misiņš, e-IT2
#
# 4.3. Handling text and symbols using tuples:
# Write a program that reads a file and prints the letters in decreasing order of frequency.
# Your program should convert all the input to lower case and only count the letters a-z.
# Your program should not count spaces, digits, punctuation, or anything other than the letters a-z.
# Find text samples from several different languages and see how letter frequency varies between languages.
import glob
import os
import sys
import pandas as pd

LANGUAGE_NAMES = {'ENG': 'English', 'ESP': 'Spanish', 'FRA': 'French', 'GER': 'German',
                  'ITA': 'Italian', 'LAT': 'Latin', 'POL': 'Polish', 'BAS': 'Basque',
                  'TUR': 'Turkish', 'LVA': 'Latvian', 'GAE': 'Gaelic', 'HUN': 'Hungarian',
                  'LIT': 'Lithuanian'}
OUTPUT_FILE_NAME = 'letter_frequencies.txt'
OUTPUT_DATAFRAME_NAME = 'letter_frequencies.xlsx'
OUTPUT_SHEET_NAME = 'Letter frequencies in %'
# SOURCE_FILE_MASK = r'4_3-genesis_1-10_*.txt'
SOURCE_FILE_MASK = r'4_3_GDPR*.txt'             # path to source files need to be defined as r-strings


def read_texts(text_file_mask):
    #
    # The last three characters (not the extension!) of a file name identify the language.
    # For example, some_text_POL.txt refers to a text in Polish
    #
    all_files = glob.glob(text_file_mask)  # since we have multiple logfiles, we need to process them all
    letters = []
    lang_names = []
    language_totals = dict()
    char_frequencies = dict()

    print('Loading and processing ' + str(len(all_files)) + ' text sources')

    #
    # Identify the complete set of letters from all texts.
    # count the total number of letters in each of the texts.
    #
    for text_file_name in all_files:
        try:
            text_file = open(text_file_name, encoding='utf-8')
        except OSError:
            print('*** ERROR: cannot open mailbox file ', text_file_name)
            quit(1)
        letter_count = 0
        for row in text_file:
            row = row.lower()
            for ch in row:
                if ch.isalpha():
                    letter_count = letter_count + 1
                    if ch not in letters:
                        letters.append(ch)
        text_file.close()
        language_key = text_file_name[-7:-4]
        language_totals[LANGUAGE_NAMES[language_key]] = letter_count
        lang_names.append((LANGUAGE_NAMES[language_key]))

    letters.sort()
    lang_names.sort()
    #
    # now when total set of letters is known,
    # open the input files again, and count occurrences of each character
    #
    for text_file_name in all_files:
        try:
            text_file = open(text_file_name, encoding='utf-8')
        except OSError:
            print('*** ERROR: cannot open mailbox file ', text_file_name)
            quit(1)
        #
        # build a temporary dictionary for the language
        #
        tmp_dict = dict()
        for lt in letters:              # initialize temporary dictionary
            tmp_dict[lt] = 0
        for row in text_file:
            row = row.lower()
            for ch in row:
                if ch.isalpha():
                    tmp_dict[ch] = tmp_dict[ch] + 1
        text_file.close()
        language_key = LANGUAGE_NAMES[text_file_name[-7:-4]]
        for lt in tmp_dict:
            tmp_dict[lt] = tmp_dict[lt]/language_totals[language_key]
        char_stats = tmp_dict.items()
        char_frequencies[language_key] = char_stats
    return lang_names, letters, char_frequencies


def print_result(results, languages, output=sys.stdout):
    #
    # output the results, either to the screen (stdout), or to
    # file specified in output
    #
    for k in languages:
        print("{} ".format(k), end="", file=output)
        for lt in results[k]:
            print(" {} {:.2%},".format(lt[0], lt[1]), end="", file=output)
        print(file=output)


def create_dataframe(results, characters, languages):
    #
    # build a Pandas dataframe. Arguments passed:
    # results - letter frequency data
    # characters - total set of characters (to be used as row indices)
    # languages - language names used (to be used as column labels)
    #
    local_df = pd.DataFrame(columns=languages, index=characters)          # create a dataframe using languages for column labels and characters for row labels
    for k in languages:
        for lt in results[k]:
            local_df.loc[lt[0], k] = float(lt[1])*100 # cell_value.format(lt[1])        # loop through the frequencies and update the respective cells for the datframe
    return local_df


#
# main body of the program
#
os.chdir(os.path.dirname(__file__))
giant_tuple = read_texts(SOURCE_FILE_MASK)        # a tuple is used to return two values from the function read_texts()

loaded_languages = giant_tuple[0]           # list of loaded languages
character_set = giant_tuple[1]              # complete set of characters identified
result_map = giant_tuple[2]                 # letter frequency results
print('> languages loaded: ', loaded_languages)
print('> characters identified: ', character_set)

print_result(result_map, loaded_languages)  # display the letter frequencies

try:
    with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as output_file:
        print_result(result_map, loaded_languages, output_file)        # write the letter frequency data to output file
except OSError:
    print('*** ERROR: cannot open output file ', OUTPUT_FILE_NAME)
    quit(1)

df = create_dataframe(result_map, character_set, loaded_languages)      # create Pandas dataframe with the results

writer = pd.ExcelWriter(OUTPUT_DATAFRAME_NAME, engine='xlsxwriter')
df.to_excel(writer, sheet_name=OUTPUT_SHEET_NAME)
writer.save()


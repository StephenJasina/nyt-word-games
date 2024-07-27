import argparse
import itertools
import sys


def parse_input(letters: str):
    letters_required = []
    letters_allowed = []
    is_required = False
    for c in letters:
        c = c.lower()
        if is_required:
            if c == ']':
                is_required = False
            elif c.isalpha():
                letters_required.append(c)
                letters_allowed.append(c)
            else:
                raise Exception
        else:
            if c == '[':
                is_required = True
            elif c.isalpha():
                letters_allowed.append(c)
            else:
                raise Exception

    letters_required = ''.join(
        c for c, _ in itertools.groupby(sorted(letters_required))
    )
    letters_allowed = ''.join(
        c for c, _ in itertools.groupby(sorted(letters_allowed))
    )
    return letters_required, letters_allowed

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        'letters',
        help='''
        List of the permitted letters, with the required one in brackets.
        For example, "a[b]cehkl" (without quotes)
        '''
    )

    arguments = argument_parser.parse_args()

    try:
        letters_required, letters_allowed = parse_input(arguments.letters)
    except:
        print('Invalid input format')
        sys.exit(0)

    with open('words.txt', 'r') as f:
        for word in f.readlines():
            word = word.rstrip()
            letters_word = set(word)
            is_valid = True

            # Check if the word is of the right length
            if len(word) < 4:
                is_valid = False

            # Check that the required letter is used
            if is_valid:
                for letter_required in letters_required:
                    if letter_required not in letters_word:
                        is_valid = False
                        break

            # Check that only the allowed letters are used
            if is_valid:
                for letter_word in letters_word:
                    if letter_word not in letters_allowed:
                        is_valid = False
                        break
            if is_valid:
                print(word)

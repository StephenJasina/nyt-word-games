import argparse
import sys


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        'letters',
        nargs='*',
        help='''
        Lists of the letters on the sides of the box.
        For example, "tud loa cip rkn" (without quotes)
        '''
    )

    arguments = argument_parser.parse_args()
    letter_groups = arguments.letters

    # Check input validity
    if len(letter_groups) < 2:
        print('Need at least two groups of letters')
        sys.exit(0)
    letters_to_index = {}
    for index, letter_group in enumerate(letter_groups):
        for letter in letter_group:
            if letter in letters_to_index:
                print(f'Repeat letter ({letter}) not allowed')
                sys.exit(0)
            letters_to_index[letter] = index
    n_letters = len(letters_to_index)
    letters_allowed = list(sorted(letters_to_index))

    with open('words.txt', 'r') as f:
        words_allowed = {
            c: []
            for c in letters_allowed
        }
        for word in f.readlines():
            word = word.rstrip()
            is_valid = True

            # Check if the word is of the right length
            if len(word) < 3:
                is_valid = False

            # Check that consecutive letters are from different groups
            if is_valid:
                index = -1
                for c in word:
                    if c not in letters_to_index:
                        is_valid = False
                        break
                    index_next = letters_to_index[c]
                    if index == index_next:
                        is_valid = False
                        break
                    index = index_next

            if is_valid:
                words_allowed[word[0]].append(word)

    # Check for one word solutions
    done = False
    for letter_initial in letters_allowed:
        for word in words_allowed[letter_initial]:
            if len(set(word)) == n_letters:
                print(word)
                done = True
    if done:
        sys.exit(1)

    # Find all two letter words
    for letter_initial in letters_allowed:
        for word_0 in words_allowed[letter_initial]:
            letters_word_0 = set(word_0)
            for word_1 in words_allowed[word_0[-1]]:
                if len(letters_word_0.union(word_1)) == n_letters:
                    print(f'{word_0} -> {word_1}')

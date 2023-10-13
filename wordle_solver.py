from tqdm import tqdm
import json

#converts a string pattern into a list pattern format
def string_to_pattern(string_pattern):
    pattern = []
    for i in string_pattern:
        if i == 'g':
            pattern.append(1)
        elif i == 'y':
            pattern.append(2)
        else:
            pattern.append(3)
    return pattern

#prints out a dictionary sorted by the values from least to greatest
def print_sort_dict(dict, n_top=20):
    values = sorted(dict.values(), reverse=False)
    keys = list(dict.keys())
    n = 0
    for value in values:
        for key in keys:
            if value == dict[key] and n <= n_top:
                n += 1
                keys.pop(keys.index(key))
                print('\t', key, ': ', round(value, 3), sep='')

# Finds all words within a wordlist that are still valid for a given pattern
def find_valid_words(word_list, word, pattern):
    words = []
    green_letters = dict()
    for i in range(5):
        if word[i] not in green_letters.keys():
            green_letters[word[i]] = 0
        if (pattern[i] == 1 or pattern[i] == 2) and (green_letters[word[i]] == 0):
            green_letters[word[i]] = 1
        elif word[i] in green_letters.keys() and (pattern[i] == 1 or pattern[i] == 2):
            green_letters[word[i]] += 1

    for test_word in word_list:
        valid = True
        for place in range(5):
            # green
            if pattern[place] == 1 and test_word[place] != word[place]:
                valid = False
                break
            # yellow
            elif pattern[place] == 2 and (word[place] not in test_word or word[place] == test_word[place]):
                valid = False
                break
            # grey
            elif pattern[place] == 3 and word[place] in test_word and test_word.count(word[place]) > green_letters[word[place]]:
                valid = False
                break

        if valid:
            words.append(test_word)
    return words

# generates the best next guess
def guess_word(word_list, pattern_list, valid_words, progress=False):
    """
    brute force approach to finding the next best guess, itterates over every possible guess, then over every possible pattern for that guess, 
    then creates a score based on the average length of the number of valid words left after that guess (for every single possible result). 
    Returns the lowest score as the best guess, as well as a score dictionary containing vairious words and their corresponding scores.
    """

    # if the benifit of eliminating valid words is outweighed by the chance of guessing the correct word, then guess from valid words
    length = len(valid_words)
    highscore = 9999999
    score_dict = dict()
    guess = ''
    best_guess_found = False

    if length == 0:
        print('User Error 0, no valid words remaining, make sure you entered everything correctly')
        return score_dict, guess, highscore

    if progress:
        pbar = tqdm(desc='Loading... ', total=len(word_list))

    if length == 1:
        score_dict[valid_words[0]] = 1.0
        guess, highscore = valid_words[0], 0.0
        return score_dict, guess, highscore

    for word in word_list:
        score = 0

        for pattern in pattern_list:
            new_valid_words = len(find_valid_words(valid_words, word, pattern))
            score += (new_valid_words/length)*(new_valid_words)

        if progress:
            pbar.update()

        if score < highscore and best_guess_found == False:
            guess = word
            highscore = score

        if word in valid_words:
            score_dict[word] = score
            if score == 1:
                best_guess_found = True
                guess = word

    if progress:
        pbar.close()

    return score_dict, guess, highscore


if __name__ == '__main__':

    # get word list and remaining valid words lists
    word_list = []
    for line in open('valid-wordle-words.txt'):
        word = line.strip()
        word_list.append(word)
    valid_words = word_list.copy()

    #get all possible patterns (precomputed)
    f = open('data.json')
    pattern_list = json.load(f)

    #main loop
    Continue = ''
    while Continue != 'n':

        # get entered word and pattern
        word_entered = input('Entered word: ')
        if word_entered in word_list:
            word_list.pop(word_list.index(word_entered))
        pattern = input('Enter the color pattern in order (no spaces) ("g"=green, "y"=yellow, "b"=grey/black): ')
        pattern = string_to_pattern(pattern.strip())

        # recalculate remaining valid words
        valid_words = find_valid_words(valid_words, word_entered, pattern)

        # find best guess, and print out other top guesses
        guess = guess_word(word_list, pattern_list, valid_words, True)
        print_sort_dict(guess[0])
        print('Best Guess:', guess[1], "score:", guess[2])
        Continue = input('Continue? (y/n): ')
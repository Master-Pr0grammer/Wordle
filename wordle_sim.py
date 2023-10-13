from wordle_solver import *

#Tests a word against the win word and returns a pattern
def test(guess, word):
    output=[3,3,3,3,3]
    greens=[]

    #green
    for i in range(5):
        if guess[i]==word[i]:
            output[i]=1
            greens.append(guess[i])

    #yellow
    for i in range(5):
        if guess[i] in word and guess[i]!=word[i] and guess[:i+1].count(guess[i])<=word.count(guess[i]) and greens.count(guess[i])<word.count(guess[i]):
            output[i]=2
    return output

#converts a string pattern into a list pattern format
def pattern_to_string(pattern):
    string_pattern = ''
    for i in pattern:
        if i == 1:
            string_pattern+='g'
        elif i == 2:
            string_pattern+='y'
        else:
            string_pattern+='b'
    return string_pattern

# Simulate all possible games and keep track of wins/losses
if __name__ == '__main__':

    # get word list and remaining valid words lists
    word_list = []
    for line in open('valid-wordle-words.txt'):
        word = line.strip()
        word_list.append(word)
    valid_words = word_list.copy()

    # load win words to simulate games
    win_word_list = []
    for line in open('win_words.txt'):
        word = line.strip()
        win_word_list.append(word)

    #get all possible patterns (precomputed)
    f = open('data.json')
    pattern_list = json.load(f)
    f.close()

    #main loop
    game_scores = []
    for win_word in win_word_list:
        print(f"\n\nNew Game [{win_word_list.index(win_word)+1}/{len(win_word_list)}]: {win_word}")

        valid_words = word_list
        win = False
        guess = 'lares' # this is the best first guess determined by the algorithm
        for i in range(1,7):
            pattern = test(guess, win_word)
            print(f'\tGuess {i}: {guess}, Pattern: {pattern_to_string(pattern)}')

            # Check if won
            if guess == win_word:
                win = True
                game_scores.append(i)
                break
            else: 
                # recalculate remaining valid words, and next guess if no win
                valid_words = find_valid_words(valid_words, guess, pattern)
                guess = guess_word(word_list, pattern_list, valid_words, True)[1]
        
        # add score of 7 if it did not win
        if win==False:
            game_scores.append(7)

    #print game history data
    num_loss=game_scores.count(7)
    num_win = len(game_scores) - num_loss
    print(f"win ratio: {num_win/len(game_scores):.3f}\nnumber of games won: {num_win}\nnumber of games lost: {num_loss}\nnumber of total games: {len(game_scores)}")
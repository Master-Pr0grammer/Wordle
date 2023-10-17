from wordle_solver import *
import multiprocessing

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

def run_games(win_words, word_list, pattern_list, progress=False):
    print(f'Running proccess testing {len(win_words)} games...')
    game_scores = [0,0,0,0,0,0,0]
    if progress:
        pbar = tqdm(desc='Loading... ', total=len(win_words))
    for win_word in win_words:
        valid_words = word_list
        win = False
        guess = 'lares' # this is the best first guess determined by the algorithm
        for i in range(0,6):
            pattern = test(guess, win_word)

            # Check if won
            if guess == win_word:
                win = True
                game_scores[i]+=1
                break
            else: 
                # recalculate remaining valid words, and next guess if no win
                valid_words = find_valid_words(valid_words, guess, pattern)
                guess = guess_word(word_list, pattern_list, valid_words, False)[1]
        
        # add score of 7 if it did not win
        if win==False:
            game_scores[-1]+=1
            print(f'"{win_word}" game lost')

        if progress:
            pbar.update()
    if progress:
        pbar.close()
    print(f'Simulation Results: {game_scores}')



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

    #simulate games on multiple cpu proccessors to speed up run time
    num_cores=multiprocessing.cpu_count()
    print(f'Starting {num_cores} Proccesses, simulating {len(win_word_list)} games...')
    processes=[]
    for i in range(num_cores):
        start_index=i*len(win_word_list)//num_cores
        end_index=(i+1)*len(win_word_list)//num_cores

        #add extra problems to last proccess
        if i == num_cores - 1:
            end_index += len(win_word_list) % num_cores

        p= multiprocessing.Process(target = run_games, args=[win_word_list[start_index:end_index], word_list, pattern_list, True])
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print("done")

#wordle_sim.py results
results = [[0, 1, 56, 170, 62, 0, 0],
[0, 4, 56, 177, 49, 3, 0],
[0, 0, 51, 171, 63, 3, 0],
[0, 1, 44, 171, 69, 3, 0],
[0, 1, 53, 171, 62, 2, 0],
[0, 2, 49, 176, 58, 3, 0],
[0, 1, 43, 184, 55, 6, 0],
[0, 0, 45, 172, 65, 7, 0]]
#1  2  3   4    5   6 loss

temp = [0,0,0,0,0,0,0]

for i in range(len(results)):
    for j in range(len(results[0])):
        temp[j]+=results[i][j]
results = temp
num_games = sum(temp)

average_score = 0
for i in range(len(results)):
    average_score+=(i+1)*results[i]
average_score /= num_games

print(f'Win rate {100*(num_games - results[-1])/num_games:.2f}%')
print(f'Average Score: {average_score:.3f}')
print(f'Median Score: {results.index(max(results))+1}')
def findMaxScore(scores):
    winner = 'a1'
    for i in scores:
        if scores[i] > scores[winner]:
            winner = i
    return winner

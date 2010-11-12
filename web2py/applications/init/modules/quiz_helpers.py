
def findMaxScore(scores):
    winner = 'Peter'
    for i in scores:
        if scores[i] > scores[winner]:
            winner = i
    return winner

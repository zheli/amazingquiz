def findMaxScore(scores):
    winner = 'a1'
    for i in scores:
        if scores[i] > scores[winner]:
            winner = i
    return winner

def fbModalWindow(title, content):
    return DIV(H2(title, _class='popup_title'),
        DIV(content),
        DIV(LABEL(INPUT(_value='Close', _type='button', _class='bClose'), 
            _class='popup_control_button'), _class='popup_control'),
        _id='popup_info', _style='display:none;')

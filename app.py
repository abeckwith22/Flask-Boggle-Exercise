from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)
# secret key
app.secret_key = "2jasdfij239j0asdf_jwkefjsecretkeylol"

""" logical functions """
def create_board():
    return boggle_game.make_board(5)

def getWordLength(word):
    return len(word)

""" Writing web routes here """
@app.route('/')
def show_home():
    """Display homepage"""
    session['board'] = create_board()
    session['submitted_words'] = [] # used to check for duplicates
    session['score'] = 0
    board = session['board']
    return render_template('home.html', board=board)

@app.route('/post/<formValue>/', methods=['GET'])
def validate_word(formValue):
    """ checks if word exists in boggle board array, then checks if result is already submitted """
    formValue = formValue.lower()

    board = session['board']
    submitted_words = session['submitted_words']
    score = session['score']

    result = boggle_game.check_valid_word(board, formValue)
    if formValue in submitted_words:
        return jsonify(valid_word='already-submitted')
    else:
        # appends formValue to submitted words and copies to session calculating length of word and appending to score
        length = getWordLength(formValue)
        if result != 'not-word' and result != 'not-on-board':
            score += length
            session['score'] = score
        
        submitted_words.append(formValue) 
        session['submitted_words'] = submitted_words 

        return jsonify(valid_word=result, game_score=score)
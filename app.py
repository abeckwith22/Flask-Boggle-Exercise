from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)
# secret key
app.secret_key = "2jasdfij239j0asdf_jwkefjsecretkeylol"

""" logical functions """
def create_board():
    """Creates boggle game board with specified n*n size"""
    return boggle_game.make_board(5)

def getWordLength(word):
    return len(word)

""" Writing web routes here """
@app.route('/')
def show_home():
    """Display board"""
    session['board'] = create_board()
    session['submitted_words'] = [] # used to check for duplicates
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    
    session['score'] = 0

    board = session['board']
    return render_template('home.html', board=board, highscore=highscore, nplays=nplays)

@app.route('/validate-word', methods=['POST'])
def validate_word():
    """ checks if word exists in boggle board array, then checks if result is already submitted """
    formValue = request.json['word'].lower()

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

@app.route('/post_score', methods=['POST'])
def post_score():
    
    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    print("SCORE:", score)
    print("HIGHSCORE:", highscore)
    print("NUMBER PLAYS:", nplays)
    session['nplays'] = nplays + 1
    if (score > highscore):
        session['highscore'] = score
    
    return jsonify(score > highscore)
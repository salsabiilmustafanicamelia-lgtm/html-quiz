from flask import Flask, session, redirect, url_for, request
from database_script import get_question_after
from random import randint

# quiz = 0
# last_question = 0

def index():
    # global quiz, last_question
    max_quiz = 3

    session['quiz'] = randint(1, max_quiz)
    session['last_question'] = 0

    if request.method == 'GET':
        pass
    else: #selain GET, ada POST (submit jawaban)
        pass

    return '<a href="/test">Test</a>'

def test():
    # global last_question
    result = get_question_after(session['last_question'], session['quiz'])
    if result is None or len(result) == 0:
        return redirect(url_for('result'))
    else:
        session['last_question'] = result[0]
        return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'

def result():
    return "Ini halaman hasil"

# Create application instance
app = Flask(__name__)
app.add_url_rule('/', 'index', index, methods=['POST', 'GET'])
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = "MtbnTlotpanfyk"

if __name__ == '__main__':
    app.run()
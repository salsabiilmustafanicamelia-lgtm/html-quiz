from flask import Flask, session, redirect, url_for, request, render_template
from database_script import get_question_after, get_quiz, check_answer
from random import randint, shuffle

# quiz = 0
# last_question = 0

# === UTILITY START ===

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    quiz_list = get_quiz()
    return render_template('start.html', quiz_list=quiz_list)

# === UTILITY END ===

# === SERVER START - START PAGE ===
def index():
    if request.method == 'GET':
        start_quiz(-1)
        #Akan tampilkan pilihan quiz
        return quiz_form()
    else: #selain GET, ada POST (submit jawaban)
        # 1) ambil nilai dari form, lalu taruh di variable
        quest_id = request.form.get('quiz')
        # 2) Mulai quiz
        start_quiz(quest_id)
        # 3) ke halaman test
        return redirect(url_for('test'))
# === SERVER END - TEST PAGE ==

# == TEST UTILITY START - TEST PAGE ===

def question_form(question):
    answers_list = [
        question[2],
        question[3],
        question[4],
        question[5]
        ]
    shuffle(answers_list)
    return render_template(
        'test.html',
        question=question[1],
        quest_id=question[0],
        answers_list = answers_list
    )

def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')

    session['last_question'] = quest_id
    session['total'] += 1

    if check_answer(quest_id, answer):
        session['answers'] += 1

def test():
    # global last_question
    if not('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method =='POST':
            save_answers()

        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

# === TEST UTILITY END - TEST PAGE ===

def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html

# Create application instance
import os
folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index, methods=['POST', 'GET'])
app.add_url_rule('/test', 'test', test, methods=['POST', 'GET'])
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = "MtbnTlotpanfyk"

if __name__ == '__main__':
    app.run()
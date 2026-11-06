# TUJUAN : SEGALA YANG BERKAITAN DENGAN DATABASE

import sqlite3

db_name = 'quiz.sqlite'
conn = None # Membuat Koneksi ke database
cursor = None # Cursor untuk akses database

# Mekanisme Akses Database
## Buka Database
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

## Tutup Database
def close():
    cursor.close()
    conn.close()

## Jelajah Database
def do(query):
    cursor.execute(query)

## Reset Database
def clear_db():
    open()
    query1 = '''DROP TABLE IF EXISTS quiz_content''' # Tabel penghubung
    query2 = '''DROP TABLE IF EXISTS questions''' #Tabel Questions
    query3 = '''DROP TABLE IF EXISTS quiz''' # Tabel Quiz
    do(query1)
    do(query2)
    do(query3)
    close()

## Membuat tabel
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query_create_quiz_table = '''
        CREATE TABLE IF NOT EXISTS quiz (
            id      INTEGER PRIMARY KEY,
            name    VARCHAR
            )
        '''
    query_create_questions_table = '''
        CREATE TABLE IF NOT EXISTS questions (
            id          INTEGER PRIMARY KEY,
            question    VARCHAR,
            answer      VARCHAR,
            wrong1      VARCHAR,
            wrong2      VARCHAR,
            wrong3      VARCHAR
            )
            '''
    query_create_quiz_content_table = '''
    CREATE TABLE iF NOT EXISTS quiz_content (
        id          INTEGER PRIMARY KEY,
        quiz_id     INTEGER,
        question_id INTEGER,

        FOREIGN KEY (quiz_id) REFERENCES quiz(id),
        FOREIGN KEY (question_id) REFERENCES questions(id)
    )
    '''
    do(query_create_quiz_table)
    do(query_create_questions_table)
    do(query_create_quiz_content_table)
    
    close()

## Membuat daftar pertanyaan
def add_questions():
    questions = [
        ("Organel sel yang berfungsi sebagai tempat berlangsungnya respirasi sel untuk menghasilkan energi adalah...","Mitokondria","Ribosom","Lisosom","Badan Golgi"),
        ("Proses pembuatan makanan pada tumbuhan hijau dengan bantuan cahaya matahari disebut...","Fotosintesis","Respirasi","Transpirasi","Fermentasi"),
        ("Pembuluh darah yang membawa darah kaya oksigen dari jantung ke seluruh tubuh disebut...","Arteri","Vena","Kapiler","Aorta paru"),
        ("Hewan yang memakan tumbuhan dan daging disebut...","Omnivora","Herbivora","Karnivora","Insektivora"),


        ("Hasil dari 15 x 12 adalah...","180","170","190","160"),
        ("Nilai x dari persamaan 2x + 6 = 18 adalah...","6","5","7","12"),
        ("Luas persegi panjang dengan panjang 12 cm dan lebar 8 cm adalah...","96 cm²","40 cm²","20 cm²","80 cm²"),
        ("Hasil dari 3/4 + 1/4 adalah...","1","3/8","4/8","1/2"),


        ("She ___ to school every day.","goes","go","going","gone"),
        ("What is the past tense of the verb 'eat'?","ate","eated","eaten","eating"),
        ("The opposite of 'happy' is...","sad","angry","excited","glad"),
        ("I ___ a book when my friend called me yesterday.","was reading","am reading","read","have read")
    ]

    open()
    cursor.executemany(
        '''
        INSERT INTO questions(
            question, answer, wrong1, wrong2, wrong3)
            VALUES(?, ?, ?, ?, ?)
        ''', questions
    )
    conn.commit()
    close()

## Membuat daftar Type Quiz
def add_quiz():
    quizes = [
        ('Biologi',),
        ('Matematika',),
        ('Bahasa Inggris',)
    ]

    open()
    cursor.executemany(
        '''
        INSERT INTO quiz
        (name) VALUES (?)
        ''', quizes
    )
    conn.commit()
    close()

## Membuat hubungan antara Pertanyaan dan Type Quiz
def add_links():
    link = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (3, 9),
        (3, 10),
        (3, 11),
        (3, 12),
    ]

    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    cursor.executemany(
        '''
        INSERT INTO quiz_content(quiz_id, question_id) VALUES (?, ?)
        ''', link
    )
    conn.commit()
    close()
    print('Data seeded successfuly')

## Apa yang diperlukan untuk menampilkan pertanyaan berikutnya
#Nomor quiz (quiz id) & nomor pertanyaan yang sudah ditanyakan
def get_question_after(question_id=0, quiz_id=1):
    open()
    query = '''
        SELECT 
            quiz_content.id,
            questions.question,
            questions.answer,
            questions.wrong1,
            questions.wrong2,
            questions.wrong3
        FROM
            questions,
            quiz_content
        WHERE
            quiz_content.question_id == questions.id
            AND quiz_content.id > ?
            AND quiz_content.quiz_id == ?
        ORDER BY
            quiz_content.id
    '''

    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone() #Mengambil 1 dari semua data
    close()
    return result

## Entry Point untuk menjalankan program
def main():
  clear_db()
  create()
  add_questions()
  add_quiz()
  add_links()
  #get_question_after(question_id = 0, quiz_id = 1)
  print(get_question_after(3, 2))

if __name__ == "__main__":
  main()
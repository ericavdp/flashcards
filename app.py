from flask import Flask, render_template, request
import pymysql
import pymysql.cursors
from random import randint

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showMakeCard')
def showMakeCard():
    return render_template('makeCard.html')


@app.route('/makeCard', methods=['POST', 'GET'])
def makeCard():
    #    conn = mysql.connect()
    conn = pymysql.connect(user='*', passwd='*', db='*', unix_socket='/tmp/mysql.sock',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    try:
        _question = request.form['inputQuestion']
        _answer = request.form['inputAnswer']
        _tags = request.form['inputTags']
        _confidence = request.form['inputConfidence']
        if _question and _answer and _tags and _confidence:
            cursor.execute(""" INSERT INTO card (question, answer, tags, confidence)  
            VALUES (%s, %s, %s, %s)""", (_question, _answer, _tags, _confidence))
            conn.commit()
            # cursor.close()
            # conn.close()
            print('boop')
            return

        else:
            print('enter the required fields')
            return

    except BaseException:
        print('it broke :(')
        return

    finally:
        cursor.execute("SELECT COUNT(*) FROM card")
        boop = cursor.fetchone()
        print('count of rows is ', boop)
        print(boop.values())
        moo = boop['COUNT(*)']
        print(moo)
        shuffle = randint(0, moo)
        print(shuffle)
        cursor.execute("SELECT * FROM card WHERE id = %s", [shuffle])
        yup = cursor.fetchone()
        print(yup)
        cursor.close()
        conn.close()
        print('fin')
        return render_template("success.html")


@app.route('/showReviewCards')
def showReviewCards():
    return render_template('reviewcards.html')


@app.route('/displayCard', methods=['POST', 'GET'])
def displayCard():
    conn = pymysql.connect(user='*', passwd='*', db='*', unix_socket='/tmp/mysql.sock',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM card")
    boop = cursor.fetchone()
    print('count of rows is ', boop)
    print(boop.values())
    moo = boop['COUNT(*)']
    print(moo)
    shuffle = randint(0, moo)
    print(shuffle)
    cursor.execute("SELECT * FROM card WHERE id = %s", [shuffle])
    yup = cursor.fetchone()
    print(yup)
    question = yup['question']
    answer = yup['answer']
    tags = yup['tags']
    confidence = yup['confidence']
    cursor.close()
    conn.close()
    print('fin')
    return render_template('showCard.html', question=question, answer=answer, tags=tags, confidence=confidence)


@app.route('/showAnswer', methods=['POST', 'GET'])
def showAnswer():
    _confidence = request.form['confidence']
    _answer = request.form['answer']
    return render_template('showAnswer.html', answer=_answer, confidence=_confidence)

@app.route('/updateCard', methods=['POST', 'GET'])
def updateCard():
    conn = pymysql.connect(user='*', passwd='*', db='*', unix_socket='/tmp/mysql.sock',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    try:
#create new table for historical confidence and timestamp
        _confidence = request.form['inputConfidence']
        if _confidence:
            #update the confidence value to new value, archive old confidence value?
           # cursor.execute(""" INSERT INTO card (question, answer, tags, confidence)
           # VALUES (%s,)""", (_question, _answer, _tags, _confidence))
           # conn.commit()
            #insert a timestamp
            print('boop')
            return

        else:
            print('enter the required fields')
            return

    except BaseException:
        print('it broke :(')
        return

    finally:
        cursor.close()
        conn.close()
        return render_template("reviewCards.html")
# def selectNextCard():
# random selection based on index number (training case)
# selection based on time and confidence level (assumption case)
#display needs to update a time stamp

# def trainAlgorithm():
# Baysian confidence training around time vs confidence

if __name__ == '__main__':
    app.run()

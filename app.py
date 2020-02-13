from flask import Flask, render_template, request, flash, redirect
import utils
from utils import render_table, fetch_question

import table_content
from forms import AnswerForm, PatchKeyForm
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.des_key


@app.route('/stage3/FEF04FA6F773F6AAEA5C3A763E2A1706', methods=['GET'])
def video_play():
    return render_template(
        'index.html',
        table=-1, option=0,
    )


@app.route('/stage2/<string:encrypted>', methods=['GET', 'POST'])
def key_to_the_door(encrypted: str):
    patch_key_query = PatchKeyForm.PatchKeyForm()
    if request.method == 'GET':
        return render_template(
            'index.html',
            table_content=render_table(26),
            table=1, option=-1, query_form=patch_key_query,
            question=fetch_question(0),
            progress_value=0
        )
    else:
        key1 = request.form.get('Key1')
        key2 = request.form.get('Key2')
        key3 = request.form.get('Key3').strip(' ')
        if key1 != config.key1 or key2 != config.key2 or key3.capitalize() != config.key3:
            flash('Your answer is: {},{},{}. Not correct.'.format(key1, key2, key3), 'error')
            return redirect('/stage2/start')
        return redirect('/stage3/FEF04FA6F773F6AAEA5C3A763E2A1706')


@app.route('/stage/<string:encrypted>', methods=['GET', 'POST'])
def hello_world(encrypted: str):
    basic_query = AnswerForm.SubmitForm()
    if request.method == 'GET':
        # stage decrypted
        # basic_query = AnswerForm.SubmitForm()
        if encrypted != 'start':
            code, result = utils.dispatch_final_stage_status(encrypted)
            code = int(code)
            if code == -1:
                return render_template('errors.html')
            if code == 99:
                return redirect('/stage2/start')
            return render_template(
                'index.html',
                table_content=render_table(code + 1),
                table=1, option=1, query_form=basic_query,
                question=fetch_question(code + 1),
                progress_value=4 * code + 4
            )
        else:
            # start the game!
            return render_template(
                'index.html',
                table_content=render_table(1),
                table=1, option=1, query_form=basic_query,
                question=fetch_question(1),
                progress_value=4
            )
        return render_template('errors.html')
    else:
        question_id = int(request.form.get('question_id'))
        length_limit = int(request.form.get('length_limit'))
        input_answer = request.form.get('InputField')
        if length_limit != len(input_answer):
            flash('Your answer is: {} with length {}, but the length of this point is {}.'.format(input_answer,
                                                                                                  len(input_answer),
                                                                                                  length_limit),
                  'error')
            if question_id == 0:
                return redirect('/stage/start')
            encrypted = '{}/{}{}'.format(question_id, '1' * (question_id),
                                         '0' * (config.total_rounds - question_id))
            hex_encrypted = utils.DES_encrypt(encrypted).decode('utf-8')
            return redirect('/stage/{}'.format(hex_encrypted))
        if input_answer != table_content.question_answer[question_id][1]:
            print('[{}]->[{}]'.format(input_answer, table_content.question_answer[question_id][1]))
            flash('Your answer is: {}, but it is wrong.'.format(input_answer), 'error')
            if question_id == 0:
                return redirect('/stage/start')
            encrypted = '{}/{}{}'.format(question_id, '1' * question_id,
                                         '0' * (config.total_rounds - question_id))
            hex_encrypted = utils.DES_encrypt(encrypted).decode('utf-8')
            return redirect('/stage/{}'.format(hex_encrypted))
        flash('Your answer is: {}, Correct!'.format(input_answer), 'error')
        encrypted = '{}/{}{}'.format(question_id + 1, '1' * (question_id + 1),
                                     '0' * (config.total_rounds - question_id - 1))
        hex_encrypted = utils.DES_encrypt(encrypted).decode('utf-8')
        return redirect('/stage/{}'.format(hex_encrypted))


@app.route('/render_test')
def render_test_table():
    m = 10
    n = 10
    word_list = [['E', 1, 2], ['W', 1, 3]]
    orange_list = [(6, 7), (6, 8)]
    blue_list = [(9, 3), (1, 3)]
    return render_template('index.html', table_content=render_table(m, n, word_list, orange_list, blue_list), table=1)


if __name__ == '__main__':
    app.run(debug=True)

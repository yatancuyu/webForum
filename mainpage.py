# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from db_workspace import DataBase
import sqlite3
from datetime import datetime

db = DataBase(sqlite3.connect('forum.db', check_same_thread=False))

admins = ['Vladislav', 'a_makushin']

class SigninForm(FlaskForm):
    username = StringField('Введите логин.', validators=[DataRequired('Это поле обязательно к заполнению.')])
    password = PasswordField('Введите пароль.', validators=[DataRequired('Это поле обязательно к заполнению.')])
    submit = SubmitField('Войти')

    def validate_username(self, field):
        if field.data not in db.get_usernames():
            raise ValidationError('Неверный логин или пароль')


class SignupForm(FlaskForm):
    username = StringField('Введите логин.')
    password = PasswordField('Введите пароль.',
                             validators=[DataRequired('Это поле обязательно к заполнению.'),
                                         EqualTo('password_check', message='Пароли не совпадают')])
    password_check = PasswordField('Введите пароль еще раз.',
                                   validators=[DataRequired('Это поле обязательно к заполнению.')])
    question = SelectField("Выберите секретный вопрос.",
                           choices=[("Как звали мальчика или девочку которую вы впервые поцеловали?",
                                     "Как звали мальчика или девочку которую вы впервые поцеловали?"),
                                    ("Какая кличка, порода и цвет вашего питомца?",
                                     "Какая кличка, порода и цвет вашего питомца?"),
                                    ("Какой город, область и район вашего места рождения?",
                                     "Какой город, область и район вашего места рождения?"),
                                    ("Какую школу вы посещали в шестом классе?",
                                     "Какую школу вы посещали в шестом классе?")
                                    ])
    answer = StringField('Введите ответ на секретный вопрос',
                         validators=[DataRequired('Это поле обязательно к заполнению.')])
    submit = SubmitField('Зарегестрироваться')

    def validate_password(self, field):
        if not (8 <= len(field.data) <= 16):
            raise ValidationError('Пароль должен иметь длину от 8 до 16 символов')
        if not (any(filter(lambda x: x in "0123456789", field.data))):
            raise ValidationError('В пароле должна присутствовать хоть одна цифра')
        if any(filter(lambda x: x in "абвгдеёийклмнопростуфхчщцьыъэюя", field.data)):
            raise ValidationError('Символы кирилицы не допускаются')

    def validate_username(self, field):
        if not (8 <= len(field.data) <= 16):
            raise ValidationError('Логин должен иметь длину от 8 до 16 символов')
        if not field.data:
            raise ValidationError('Это поле обязательно к заполнению.')
        if field.data in db.get_usernames():
            raise ValidationError('Это имя уже занято.')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    userform = SignupForm()
    if request.method == "GET":
        return render_template("signup.html", form=userform, title="Регистрация")
    if request.method == "POST" and userform.validate_on_submit():
        db.insert_user(userform.username.data, userform.password.data, userform.question.data, userform.answer.data)
        session["username"] = userform.username.data
        return redirect("/main")
    if not userform.validate_on_submit():
        return render_template("signup.html", form=userform, title="Регистрация")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    userform = SigninForm()
    if request.method == "GET":
        return render_template("signin.html", form=userform, title="Авторизация")
    if request.method == "POST" and userform.validate_on_submit():
        session["username"] = userform.username.data
        return redirect("/main")
    if not userform.validate_on_submit():
        return render_template("signin.html", form=userform, title="Авторизация")


@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html", title="Форум", sections=db.get_sections_info())


@app.route('/signout')
def signout():
    del session["username"]
    return redirect("\main")


@app.route('/section/<string:section>/')
def section(section):
    if section in [i[2] for i in db.get_sections_info()]:
        return render_template("section.html", title=section, section=db.get_sections_info(section)[1],
                               sec=section,
                               topics=db.get_topics_info(db.get_sections_info(section)[0]), str=str)


@app.route('/section/<section>/<int:topic_id>', methods=['POST', 'GET'])
def topic(section, topic_id):
    if request.method == 'GET':
        mass = db.get_messages(topic_id)
        db.plus_view(topic_id)
        print(mass)
        return render_template('topic.html', messages=mass, session=session)
    elif request.method == 'POST':
        db.insert_message(session['username'], int(topic_id), request.form['message'], ''.join(str(datetime.now()).split('.')[:-1]))
        mass = db.get_messages(topic_id)
        return redirect('/section/{}/{}'.format(section, topic_id))
    else:
        return redirect('/section/{}/{}'.format(section, topic_id))



@app.route('/section/<section>/add_topic', methods=['POST', 'GET'])
def add_topic(section):
    if request.method == 'GET':
        return render_template('add_topic.html', section_name=section, session=session)
    elif request.method == 'POST':
        db.insert_topic(int(db.get_sections_info(section)[0]), request.form['WTF'], request.form['about'], session["username"], ''.join(str(datetime.now()).split('.')[:-1]))
        return redirect('/section/{}'.format(section))
    else:
        return redirect('/section/{}'.format(section))


@app.route('/del_user', methods=['POST', 'GET'])
def del_user():
    if request.method == 'GET':
        return render_template('admin.html', session=session, admins=admins)
    elif request.method == 'POST':
        db.delete(request.form['user'])
        return redirect('/main')



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

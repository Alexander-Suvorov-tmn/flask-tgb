import os
import random

import requests
import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from db import connected
from db import db

if os.path.exists(config.DOTENV_PATH):
    load_dotenv(config.DOTENV_PATH)

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
# app.config.from_object(os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'send-error'


class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(login):
    return User(login)


@app.route('/', methods=['POST', 'GET'])
# @login_required
def index():
    data = request.values
    return render_template('choice.html')


@app.route('/choice', methods=['POST', 'GET'])
def choice():
    '''
    страница выбора (получить код - если уже зареген в телеге либо регистрация в телеге)
    '''
    user_data = db.botkey.get('id', request.values[request.args.get('user_id')])
    if not user_data:
        return render_template('choice.html',
                               message='Вам необходимо пройти регистрацию в мессенджере Telegram для получения '
                                       'пароля. Для этого в Telegram в поиске наберите @Yamata_telegram_bot и '
                                       'следуйте инструкции')
    if user_data['telegram_id']:
        key = random.randint(1111, 9999)
        db.botkey.update(request.values['id'], key)
        requests.post(os.environ.get('URL_SET'), {'chat_id': user_data['telegram_id'], 'text': key})
        return render_template(
            'key.html', id=request.form['user_id'],
            message='Вам отправлен пароль для входа в Telegram, проверьте пожалуйста сообщения от Yamata'
        )
    else:
        return render_template('choice.html',
                               message='Вам необходимо пройти регистрацию в мессенджере Telegram для получения '
                                       'пароля. Для этого в Telegram в поиске наберите @Yamata_telegram_bot и '
                                       'следуйте инструкции')


@app.route('/key', methods=['POST', 'GET'])
def get_key():
    '''
    страница ввода пароля, полученного в телеге
    '''
    return render_template('key.html')



@app.route('/entrance', methods=['POST', 'GET'])
def entrance():
    '''
    обрабатываем введенный пароль
    '''
    for key in request.form:
        if request.form[key] == '':
            return render_template('entrance.html', message='Пароль не введен')

    answer = db.botkey.get(request.form['id'])
    if answer['key'] == request.form['key']:
        return render_template('index.html', message='Добро пожаловать!')
    else:
        return render_template('entrance.html', message='Введен не верный пароль!')


@app.route('/get_data', methods=['POST', 'GET'])
def get_data():
    requests.get("https://api.telegram.org/bot5031875066:AAFlPRGfzlRJplNSRSYGKh78xnWvJzAk3cY/getUpdates")
    return


@app.route('/about')
# @login_required
def about():
    return render_template('about.html')


@app.route("/logout")
# @login_required
def logout():
    logout_user()
    return 'Пока'


@app.teardown_appcontext
def shutdown_session(exception=None):
    '''
    Flask автоматически удалит сеансы базы данных в конце запроса или при завершении работы приложения
    '''
    connected.sess.remove()


# Set_webhook
# @app.route('/set_webhook', methods=['GET', 'POST'])
# def set_webhook():
    # '''
    # *set_webhook - отвечает за создание вебхука с сервером Telegram и вызывается один раз.
    # *get_key - слушает на /key и занимается обработкой сообщений с серверов телеграма.
    # В хендлере мы получаем данные в Post запросе, достаем нужную информацию и исходя из этого
    # делаем какие-то действия и шлем сообщение юзеру методом bot.send_message.
    #
    # '''
#     s = bot.setWebhook('https://%s:443/HOOK' % URL, certificate=open('/etc/ssl/server.crt', 'rb'))
#     if s:
#         print(s)
#         return "webhook setup ok"
#     else:
#         return "webhook setup failed"


if __name__ == '__main__':
    app.run()

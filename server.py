from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
from random import choice
from data import db_session, gg_api
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user
from fast_or_slow import slowfast_music
from revers import reverse_audio_file
from bass import bass_boost
from nonoise import remove_noise
from reverb import reverb_sound
from eqalazer import equalizer
from grossbit import gross_bit
from deletenenuzn import cuttingnenuznogo
from obrezka import obrezka
from effects import effects

app = Flask(__name__)

upload_folder = os.path.join('static', 'snd')
extensions = ['mp3', 'wav', 'ogg', 'flac']  # Подходящие расширения

if __name__ == '__main__':
    db_session.global_init("db/users.sqlite")  # Подключение к БД
    app.register_blueprint(gg_api.gg)  # н̧̘̯̝͈̣̃̄́̈́͘͢͝͠е̡͈͕̘͓͈̯̪͐̋̀̓̿̎͛͗ ̢͚̦̮̻̀͛̒̿̄
    # в̻̙̩̺͈̩̾̒̇͊͑͞к̛͓͕̖͉̰̫̖͓̋͛́̿͂͘͝л̧̨̀̕ю̬͙̖̦̈́͒̀̕
    # ч̧̢̲͎̥̙̓̅͂͒̅͋а̲̥̱͍͓͈̄̈̄͛̅͌͂͟т̥̰̰͖̬͈͑́̾͂̌̀͆ͅь̗̝͓̙̞͉͆̉͐̇̀̄̈̓͢͢,̢̬̻̞͎̻̐̒͑̾̉̚͜͠ ̧̛͕̣̥̱͑́̀̎
    # о̤̳̞̙͕̥̐̒̿̅̏̒п̩̓а̻̗̳̭̝̬͎̳͊̊̄͋͊̉̉̊̾͜с͓͕͉̃̕͡н̨͕̗̝̪̮͍̲̭̂̌̎́̋̑̉̿͐̃͢о̡̨̢̳̻̘̘̼̞̖̋̿͐̀͆͒͐̈́̈̇

# Диапазоны функций работы со звуком
bass_diapason = range(1, 101, 1)
fast_slow_diapason = \
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
noise_diapason = range(1, 21, 1)
reverb_diapason = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

app.config['UPLOAD'] = upload_folder
app.config['SECRET_KEY'] = 'forsoul_secretkey'
app.config['MAX_CONTENT_LENGTH'] = 32000000  # 32 МБ - максимальный размер
login_manager = LoginManager()
login_manager.init_app(app)

audio_sound = ''  # Путь до текущего звука
new_sound = ''  # Путь до нового звука


@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', error='Вы не авторизованы в системе')


@app.errorhandler(413)
def too_large(error):
    return render_template('error.html', error='Файл слишком большой. (максимум 32 МБ)')


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Недопустимые значения в пароле
        easy_numbers = ['0123456789'[number:number + 3] for number in range(8)]
        rus_letters = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
        easy_rus = [rus_letters[ru:ru + 3] for ru in range(31)]
        eng_letters = 'qwertyuiopasdfghjklzxcvbnm'
        easy_eng = [eng_letters[en:en + 3] for en in range(24)]

        # Проверка пароля на правильность (отдельная функция не работает)

        # Проверка на наличие 123, йцукен, qwerty и т. д.
        for num in easy_numbers:
            if num in form.password.data:
                return render_template('register.html',
                                       form=form,
                                       message="Пароль слишком лёгкий (цифры)")
        for eng in easy_eng:
            if eng in form.password.data:
                return render_template('register.html',
                                       form=form,
                                       message="Пароль слишком лёгкий (английские буквы)")
        for rus in easy_rus:
            if rus in form.password.data:
                return render_template('register.html',
                                       form=form,
                                       message="Пароль слишком лёгкий (русские буквы)")

        # Проверка на длину
        if len(form.password.data) < 8:
            return render_template('register.html',
                                   form=form,
                                   message="Пароль слишком короткий")

        # Проверка на одинаковые буквы
        last_letter = ''
        let_count = 0
        for let in form.password.data:
            if let_count == 0:
                let_count += 1
            elif let_count != 0 and let == last_letter:
                let_count += 1
            else:
                let_count = 0
            if let_count == 3:
                return render_template('register.html',
                                       form=form,
                                       message="Пароль слишком лёгкий (много одинаковых букв)")
            last_letter = let

        # Проверка правильности введённых данных
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(login=form.login.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


# Login Manager
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


# Выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Главная страница
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global audio_sound, new_sound  # Путь до старого и нового файлов записывается в
    # глобальную переменную, иначе сайт их не распознаёт

    # Удаление файлов после прошлой сессии
    for file in os.listdir('static/snd'):
        name = os.fsdecode(file)  # Файл
        if (name != 'fx1.wav'
                and name != 'fx2.wav'
                and name != 'fx3.wav'
                and name != 'fx4.wav'
                and name != 'fx5.wav'):  # Такие имена носят эффекты, которые можно наложить,
            # их нельзя удалять или заменять
            os.remove(f'static/snd/{name}')
    audio_sound = ''  # Обновление пути до старого файла
    new_sound = ''  # Обновление пути до нового файла

    # Загрузка файла
    if request.method == 'POST':
        file = request.files['snd']
        filename = secure_filename(file.filename)
        if filename == '':
            return render_template('error.html', error='Не выбран файл')
        if filename[-3:] not in extensions:
            return render_template('error.html', error='Неправильное расширение файла')
        elif (filename == 'fx1.wav' or
              filename == 'fx2.wav' or
              filename == 'fx3.wav' or
              filename == 'fx4.wav' or
              filename == 'fx5.wav'):  # Проверка, не носит ли файл такое же имя, как и эффект
            return render_template('error.html', error='Неправильное имя файла: '
                                                       'Имя "fx" носят 5 встроенных в сайт эффектов')
        # Сохранение файла на время сессии и перенаправление на страницу с операциями
        file.save(os.path.join(app.config['UPLOAD'], filename))
        sound = os.path.join(app.config['UPLOAD'], filename)
        audio_sound = sound
        return redirect('/redact')
    return render_template('main.html')


# Информация о сайте
@app.route('/info', methods=['GET', 'POST'])
def info():
    secret_page = choice(range(0, 1000, 1))  # э̌ͅт̛̥͓͇͒̚о ͇̪̅̈́͘ͅещ̩̞̜̖͈̾͐́͆̑ё̧̢̛̛̖̕
    # ͓͔̗̑̀͡ч̛͇̲̘͌̃т̺̺̐͘о̨̬͒̒ ̧̺̹͉̈͐̒͂я̥̒̒͢ ̢̊̉ ̳не̧̞̱͆̍̎ ̨̡̼͈̟̃̽͒̈̕
    # п̯̤̻͑̔̀л͔͔͓̝̐͌̀͘а̛͚̖͎̜́͒̄н̪̅и̹̤̏̑р̽͢о̡͍̰̊̀͂͘ͅв͙̼̜͎̐̈́̃̕а̗̺̺͔͖͐̎̑̓͡л ̡̜̿̎͘͢
    # э͚̞̕͝т̜̃о͖̠̟͂͐͝ ̟͍̻͌̓́з̩͂д͓̲͌͡е̜̩̳͛͂̀сь̰̜̻̓͗͡
    return render_template('info.html', secret_page=secret_page)


# Инструкция по пользованию сайтом
@app.route('/guide', methods=['GET', 'POST'])
def guide():
    return render_template('guide.html')


# Выбор операции
@app.route('/redact', methods=['GET', 'POST'])
@login_required
def operation_choose():
    return render_template('operation_choose.html', sound=audio_sound)


# Замедление/ускорение
@app.route('/fast_slow', methods=['GET', 'POST'])
@login_required
def fast_slow():
    global new_sound  # Путь до нового файла записывается в глобальную переменную, иначе сайт его не распознаёт
    if request.method == 'POST':
        fs_x = request.form.get("fs_percent")  # Получение значения
        try:
            if float(fs_x) not in fast_slow_diapason:
                return render_template('error.html', error='Задано значение не из диапазона')
            else:
                new_sound = slowfast_music(audio_sound, float(fs_x))
                new_sound.export('static/snd/result.wav', format="wav")
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html', error='Задано недопустимое значение')
    return render_template('fast_slow.html', sound=audio_sound)


# Разворот в обратную сторону
@app.route('/reverse', methods=['GET', 'POST'])
@login_required
def reverse():
    global new_sound
    if request.method == 'POST':
        new_sound = reverse_audio_file(audio_sound, 'static/snd/result.wav')
        os.remove(audio_sound)
        return redirect('/new_file')
    return render_template('reverse.html', sound=audio_sound)


# Усиление басов
@app.route('/bast_boost', methods=['GET', 'POST'])
@login_required
def bast_boost():
    global new_sound
    if request.method == 'POST':
        bass_x = request.form.get("bass_percent")
        try:
            if int(bass_x) not in bass_diapason:
                return render_template('error.html', error='Задано значение не из диапазона')
            else:
                new_sound = bass_boost(audio_sound, 'static/snd/result.wav', int(bass_x))
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html', error='Задано недопустимое значение')
    return render_template('bass_boost.html', sound=audio_sound)


# Удаление шума
@app.route('/no_noise', methods=['GET', 'POST'])
@login_required
def no_noise():
    global new_sound
    if request.method == 'POST':
        noise_x = request.form.get("noise_percent")
        try:
            if int(noise_x) not in noise_diapason:
                return render_template('error.html', error='Задано значение не из диапазона')
            else:
                new_sound = remove_noise(audio_sound, int(noise_x))
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html', error='Задано недопустимое значение')
    return render_template('no_noise.html', sound=audio_sound)


# Ревербация
@app.route('/reverb', methods=['GET', 'POST'])
@login_required
def reverb():
    global new_sound
    if request.method == 'POST':
        volume, mix = request.form.get("volume"), request.form.get("mix")
        try:
            if float(volume) not in reverb_diapason and float(mix) not in reverb_diapason:
                return render_template('error.html', error='Задано(ы) значение(я) не из диапазона')
            else:
                new_sound = reverb_sound(audio_sound, 'static/snd/result.wav', float(volume), float(mix))
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html', error='Задано(ы) недопустимое(ые) значение(я)')
    return render_template('reverb.html', sound=audio_sound)


# Эквалайзер
@app.route('/equalizer', methods=['GET', 'POST'])
@login_required
def music_equalizer():
    global new_sound
    # Проверка расширения файла
    if audio_sound[-3:] != 'wav':
        return render_template('equalize_error.html')
    else:
        if request.method == 'POST':
            freq_start, freq_end, freq_step = (request.form.get("freq_start"),
                                               request.form.get("freq_end"),
                                               request.form.get("freq_step"))  # Частоты
            coeff_start, coeff_end, coeff_step = (request.form.get("coeff_start"),
                                                  request.form.get("coeff_end"),
                                                  request.form.get("coeff_step"))  # Коэффициенты
            try:
                freqs = [int(freq) for freq in range(int(freq_start), int(freq_end), int(freq_step))]
                coeffs = [int(coeff) / 10.0 for coeff in range(int(coeff_start), int(coeff_end), int(coeff_step))]
                new_sound = equalizer(audio_sound, freqs, coeffs)
                os.remove(audio_sound)
                return redirect('/new_file')
            except ValueError:
                return render_template('error.html', error='Задано(ы) недопустимое(ые) значение(я)')
    return render_template('equalizer.html', sound=audio_sound)


# GrossBeat
@app.route('/gross_beat', methods=['GET', 'POST'])
@login_required
def gross_beat():
    global new_sound
    if audio_sound[-3:] != 'wav':
        return render_template('equalize_error.html')
    else:
        if request.method == 'POST':
            gs_x = request.form.get("gs_percent")
            try:
                new_sound = gross_bit(audio_sound, int(gs_x))
                os.remove(audio_sound)
                return redirect('/new_file')
            except ValueError:
                return render_template('error.html', error='Задано недопустимое значение')
    return render_template('gross_beat.html', sound=audio_sound)


# Вырезка ненужного фрагмента
@app.route('/slicer', methods=['GET', 'POST'])
@login_required
def slicer():
    global new_sound
    if request.method == 'POST':
        start1, end1, start2, end2 = (request.form.get("start_1"),
                                      request.form.get("end_1"),
                                      request.form.get("start_2"),
                                      request.form.get("end_2"))
        try:
            new_sound = cuttingnenuznogo(audio_sound, int(start1), int(end1), int(start2), int(end2))
            os.remove(audio_sound)
            return redirect('/new_file')
        except ValueError:
            return render_template('error.html', error='Задано(ы) недопустимое(ые) значение(я)')
    return render_template('slicer.html', sound=audio_sound)


# Обрезка
@app.route('/cutter', methods=['GET', 'POST'])
@login_required
def cutter():
    global new_sound
    if request.method == 'POST':
        start, end = (request.form.get("start"),
                      request.form.get("end"))
        try:
            new_sound = obrezka(audio_sound, int(start), int(end))
            os.remove(audio_sound)
            return redirect('/new_file')
        except ValueError:
            return render_template('error.html', error='Задано(ы) недопустимое(ые) значение(я)')
    return render_template('cutter.html', sound=audio_sound)


# Наложение эффектов
@app.route('/effects', methods=['GET', 'POST'])
@login_required
def set_effects():
    global new_sound
    if request.method == 'POST':
        effect_1, effect_2, effect_3, effect_4, effect_5 = (request.form.get('effect_1'),
                                                            request.form.get('effect_2'),
                                                            request.form.get('effect_3'),
                                                            request.form.get('effect_4'),
                                                            request.form.get('effect_5'))
        try:
            new_sound = effects(audio_sound, int(effect_1), int(effect_2), int(effect_3), int(effect_4), int(effect_5))
            os.remove(audio_sound)
            return redirect('/new_file')
        except ValueError:
            return render_template('error.html', error='Задано(ы) недопустимое(ые) значение(я)')
    return render_template('effects.html', sound=audio_sound)


# Страница с обработанным файлом
@app.route('/new_file', methods=['GET', 'POST'])
@login_required
def new_file():
    if os.path.exists('static/snd/result.wav') is True:
        path = 'static/snd/result.wav'
        return render_template('download.html', new_sound=new_sound, path=path)
    else:
        return render_template('error.html', error='Нет обработанного файла')


# Скачивание файла
@app.route('/download_file', methods=['GET', 'POST'])
@login_required
def download_file():
    if request.method == 'GET':
        if os.path.exists('static/snd/result.wav') is True:
            return send_file('static/snd/result.wav', as_attachment=True)
        else:
            return render_template('error.html', error='Нет файла для скачивания')


app.run()
            

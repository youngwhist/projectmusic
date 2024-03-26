from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
from fast_or_slow import slowfast_music
from revers import reverse_audio_file
from bass import bass_boost
from nonoise import remove_noise
from reverb import reverb_sound
from eqalazer import equalizer

app = Flask(__name__)

upload_folder = os.path.join('static', 'snd')
extensions = ['mp3', 'wav', 'ogg']

app.config['UPLOAD'] = upload_folder

audio_sound = ''
new_sound = ''
list_count = []  # Список параметров для эквалайзера


# Главная страница
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global audio_sound
    if os.path.exists('static/snd/result.wav') is True:
        os.remove('static/snd/result.wav')
    if os.path.exists(audio_sound) is True:
        os.remove(audio_sound)
    list_count.clear()
    if request.method == 'POST':
        file = request.files['snd']
        filename = secure_filename(file.filename)
        if filename[-3:] not in extensions:
            return render_template('error.html')
        file.save(os.path.join(app.config['UPLOAD'], filename))
        sound = os.path.join(app.config['UPLOAD'], filename)
        audio_sound = sound
        return redirect('/operation')
    return render_template('base.html')


# Выбор операции
@app.route('/operation', methods=['GET', 'POST'])
def operation_choose():
    return render_template('operation_choose.html', sound=audio_sound)


# Замедление/ускорение
@app.route('/fast_slow', methods=['GET', 'POST'])
def fast_slow():
    global new_sound
    if request.method == 'POST':
        x = request.form.get("fs_percent")
        diapason = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        try:
            if float(x) not in diapason:
                return render_template('error.html')
            else:
                new_sound = slowfast_music(audio_sound, float(x))
                new_sound.export('static/snd/result.wav', format="wav")
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html')
    return render_template('fast_slow.html', sound=audio_sound)


# Разворот в обратную сторону
@app.route('/reverse', methods=['GET', 'POST'])
def reverse():
    global new_sound
    if request.method == 'POST':
        new_sound = reverse_audio_file(audio_sound, 'static/snd/result.wav')
        os.remove(audio_sound)
        return redirect('/new_file')
    return render_template('reverse.html', sound=audio_sound)


# Усиление басов
@app.route('/bast_boost', methods=['GET', 'POST'])
def bast_boost():
    global new_sound
    if request.method == 'POST':
        x = request.form.get("bass_percent")
        diapason = range(1, 101, 1)
        try:
            if int(x) not in diapason:
                return render_template('error.html')
            else:
                new_sound = bass_boost(audio_sound, 'static/snd/result.wav', int(x))
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html')
    return render_template('bass_boost.html', sound=audio_sound)


# Удаление шума
@app.route('/no_noise', methods=['GET', 'POST'])
def no_noise():
    global new_sound
    if request.method == 'POST':
        x = request.form.get("noise_percent")
        diapason = range(1, 21, 1)
        try:
            if int(x) not in diapason:
                return render_template('error.html')
            else:
                new_sound = remove_noise(audio_sound, int(x))
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html')
    return render_template('no_noise.html', sound=audio_sound)


# Ревербация
@app.route('/reverb', methods=['GET', 'POST'])
def reverb():
    global new_sound
    if request.method == 'POST':
        x, y = request.form.get("volume"), request.form.get("mix")
        diapason = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        try:
            if float(x) not in diapason and float(y) not in diapason:
                return render_template('error.html')
            else:
                new_sound = reverb_sound(audio_sound, 'static/snd/result.wav', float(x), float(y))
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return render_template('error.html')
    return render_template('reverb.html', sound=audio_sound)


# Эквалайзер (страница 1)
@app.route('/equalize_1', methods=['GET', 'POST'])
def equalize_1():
    if audio_sound[-3:] != 'wav':
        return render_template('equalize_error.html')
    else:
        if request.method == 'POST':
            try:
                x = request.form.get("parameters")
                for i in range(int(x)):
                    list_count.append(i + 1)
                return redirect('/equalize_2')
            except ValueError:
                return render_template('error.html')
        return render_template('equalizer_1.html', sound=audio_sound)


# Эквалайзер (страница 2)
@app.route('/equalize_2', methods=['GET', 'POST'])
def equalize_2():
    global new_sound
    freqs = []
    coeffs = []
    if request.method == 'POST':
        try:
            for i in range(len(list_count)):
                x, y = request.form.get(f"freq_{i + 1}"), request.form.get(f"coeff_{i + 1}")
                freqs.append(float(x))
                coeffs.append(float(y))
            new_sound = equalizer(audio_sound, freqs, coeffs)
            os.remove(audio_sound)
            return redirect('/new_file')
        except ValueError:
            return render_template('error.html')
    return render_template('equalizer_2.html', sound=audio_sound, count=list_count)


# Страница с обработанным файлом
@app.route('/new_file', methods=['GET', 'POST'])
def new_file():
    path = 'static/snd/result.wav'
    return render_template('download.html', new_sound=new_sound, path=path)


# Скачивание файла
@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
    if request.method == 'GET':
        return send_file('static/snd/result.wav', as_attachment=True)


if __name__ == '__main__':
    app.run(port=8001)
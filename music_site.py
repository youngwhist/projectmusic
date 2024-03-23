from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
from fast_or_slow import slowfast_music

app = Flask(__name__)

upload_folder = os.path.join('static', 'snd')
extensions = ['mp3', 'wav', 'ogg']

app.config['UPLOAD'] = upload_folder

audio_sound = ''
new_sound = ''


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global audio_sound
    if request.method == 'POST':
        file = request.files['snd']
        filename = secure_filename(file.filename)
        if filename[-3:] not in extensions:
            return render_template('error.html')
        file.save(os.path.join(app.config['UPLOAD'], filename))
        sound = os.path.join(app.config['UPLOAD'], filename)
        audio_sound = sound
        return redirect('/fast_slow')
    return render_template('base.html')


# Замедление/ускорение
@app.route('/fast_slow', methods=['GET', 'POST'])
def fast_slow():
    global new_sound
    if request.method == 'POST':
        x = request.form.get("percent")
        diapason = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
        try:
            if float(x) not in diapason:
                return 'Неверный уровень изменения'
            else:
                new_sound = slowfast_music(audio_sound, float(x))
                new_sound.export('static/snd/result.wav', format="wav")
                os.remove(audio_sound)
                return redirect('/new_file')
        except ValueError:
            return 'Неверный уровень изменения'
    return render_template('file.html', sound=audio_sound)


@app.route('/new_file', methods=['GET', 'POST'])
def new_file():
    path = 'static/snd/result.wav'
    return render_template('download.html', new_sound=new_sound, path=path)


@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
    if request.method == 'GET':
        return send_file('static/snd/result.wav', as_attachment=True)


if __name__ == '__main__':
    app.run(port=8001)
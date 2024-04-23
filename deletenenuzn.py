from pydub import AudioSegment

def cuttingnenuznogo(file_path, start_time1, end_time1, start_time2, end_time2):
    audio = AudioSegment.from_file(file_path)
    kusok1 = audio[start_time1:end_time1]
    kusok2 = audio[start_time2:end_time2]
    nuznokusok = kusok1 + kusok2
    nuznokusok.export('static/snd/result.wav', format="wav")

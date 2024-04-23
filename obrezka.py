import pydub


def obrezka(file_path, start_time, end_time):
    audio = pydub.AudioSegment.from_file(file_path)
    start_time = int(start_time * 1000)
    end_time = int(end_time * 1000)
    obrezannoe = audio[start_time:end_time]
    obrezannoe.export('static/snd/result.wav', format="wav")


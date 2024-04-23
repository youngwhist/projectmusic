from pydub import AudioSegment


def remove_noise(file_path, koefbezshuma):
    audio = AudioSegment.from_file(file_path)

    reduced_audio = audio - koefbezshuma
    bezshuma = "static/snd/result.wav"
    reduced_audio.export(bezshuma, format="wav")
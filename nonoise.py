from pydub import AudioSegment


def remove_noise(file_path, koefbezshuma):
    audio = AudioSegment.from_file(file_path)

    reduced_audio = audio - koefbezshuma
    bezshuma = "audio.wav"
    reduced_audio.export(bezshuma, format="wav")


file_path = "audio.wav"
koefbezshuma = 10
remove_noise(file_path, koefbezshuma)

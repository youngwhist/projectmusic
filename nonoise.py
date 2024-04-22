from pydub import AudioSegment


def remove_noise(file_path, koefbezshuma):
    audio = AudioSegment.from_file(file_path)

    reduced_audio = audio - koefbezshuma

    reduced_audio.export(file_path, format="wav")

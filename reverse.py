from pydub import AudioSegment


def reverse_audio_filee(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    reversed_audio = audio.reverse()
    reversed_audio.export(output_file, format="wav")


file_path = "audio.wav"


from pydub import AudioSegment


def split_audio(file_path, output_voice, output_music, threshold):
    audio = AudioSegment.from_file(file_path)

    voice = audio.low_pass_filter(threshold)
    music = audio.high_pass_filter(threshold)

    voice.export(output_voice, format='wav')
    music.export(output_music, format='wav')


file_path = 'r.wav'
output_voice = 'voice.wav'
output_music = 'music.wav'
threshold = 3000
split_audio(file_path, output_voice, output_music, threshold)


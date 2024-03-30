import pydub


def obrezka(file_path, output_file, start_time, end_time):
    audio = pydub.AudioSegment.from_file(file_path)
    start_time = int(start_time * 1000)
    end_time = int(end_time * 1000)
    obrezannoe = audio[start_time:end_time]
    obrezannoe.export(output_file, format="wav")


file_path = "audio.wav"
start_time = 10
end_time = 20
obrezka(file_path, file_path, start_time, end_time)


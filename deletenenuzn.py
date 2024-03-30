from pydub import AudioSegment

def cuttingnenuznogo(file_path, start_time1, end_time1, start_time2, end_time2):
    audio = AudioSegment.from_file(file_path)
    kusok1 = audio[start_time1:end_time1]
    kusok2 = audio[start_time2:end_time2]
    nuznokusok = kusok1 + kusok2
    nuznokusok.export(file_path, format="wav")


file_path = "audio.wav"
start_time1 = 1000
end_time1 = 10000
start_time2 = 60000
end_time2 = 69000
cuttingnenuznogo(file_path, start_time1, end_time1, start_time2, end_time2)

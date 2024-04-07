from pydub import AudioSegment


def effects(file_path, sec1, sec2, sec3, sec4, sec5):
    audio = AudioSegment.from_file(file_path, format="wav")
    fx1 = AudioSegment.from_file("fx1.wav", format="wav")
    fx2 = AudioSegment.from_file("fx2.wav", format="wav")
    fx3 = AudioSegment.from_file("fx3.wav", format="wav")
    fx4 = AudioSegment.from_file("fx4.wav", format="wav")
    fx5 = AudioSegment.from_file("fx5.wav", format="wav")
    itogovoeaudio = audio.overlay(fx1, position=sec1)
    itogovoeaudio = itogovoeaudio.overlay(fx2, position=sec2)
    itogovoeaudio = itogovoeaudio.overlay(fx3, position=sec3)
    itogovoeaudio = itogovoeaudio.overlay(fx4, position=sec4)
    itogovoeaudio = itogovoeaudio.overlay(fx5, position=sec5)
    itogovoeaudio.export(file_path, format="wav")


file_path = "audio.wav"
sec1 = 1000
sec2 = 10000
sec3 = 19900
sec4 = 29000
sec5 = 39000
effects(file_path, sec1, sec2, sec3, sec4, sec5)
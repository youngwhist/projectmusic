import pydub


def slowfast_music(file_path, sootnoshenie):
    sound = pydub.AudioSegment.from_file(file_path)
    modified_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * sootnoshenie)
    })

    return modified_sound

file_path = "audio.wav"
speed = 0.7
if speed != 0:
    slowfast_sound = slowfast_music(file_path, speed)
    slowfast_sound.export(file_path, format="wav")
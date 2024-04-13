import pydub


def bass_boost(file, zabushenn, boost):
    audio = pydub.AudioSegment.from_file(file)
    boosted_audio = audio + boost
    boosted_audio.export(zabushenn, format="wav")


# file_path = "audio.wav"
# boost = 10
# bass_boost(file_path, file_path, boost)

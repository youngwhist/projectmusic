import scipy.io.wavfile
import numpy as np

def gross_bit(file_path, bit):
    # Загрузка аудио файла
    sample_rate, audio_data = scipy.io.wavfile.read(file_path)

    # Проверка и изменение битовой глубины аудио
    if bit < sample_rate:
        audio_data = audio_data / (2 ** (16 - bit))

    # Сохранение измененного аудио файла
    audio_file_path = file_path.replace('.wav', f'.wav')
    scipy.io.wavfile.write(audio_file_path, sample_rate, audio_data.astype(np.int16))


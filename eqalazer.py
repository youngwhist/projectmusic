import numpy as np
from scipy.io import wavfile


def equalizer(file_path, chastota, koeficent):
    sample_rate, data = wavfile.read(file_path)
    data = data.astype(float)
    spectrum = np.fft.fft(data)
    chastota = np.fft.fftfreq(len(data), d=1/sample_rate)
    for freq, gain in zip(chastota, koeficent):
        closest_freq = min(chastota, key=lambda x: abs(x - freq))
        index = np.where(chastota == closest_freq)[0][0]
        spectrum[index] *= gain
    equalized = np.fft.ifft(spectrum).real
    equalized = equalized.astype(np.int16)
    wavfile.write('static/snd/result.wav', sample_rate, equalized)

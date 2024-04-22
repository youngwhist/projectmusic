import numpy as np
import soundfile as sf
from scipy.signal import lfilter


def reverbb(input_file, output_file, gromkostreverba, mix):
    audio, sr = sf.read(input_file)
    reverb_signal = np.zeros_like(audio)
    delays = [int(sr * 0.01), int(sr * 0.03), int(sr * 0.05), int(sr * 0.07)]
    gains = [0.4, 0.3, 0.2, 0.1]
    for i, delay in enumerate(delays):
        delayed_audio = np.zeros_like(audio)
        delayed_audio[delay:] = audio[:-delay]
        reverb_signal += lfilter([gains[i]], 1, delayed_audio)
    wet_signal = gromkostreverba * reverb_signal
    dry_signal = (1 - mix) * audio
    output_signal = mix * wet_signal + dry_signal
    sf.write(output_file, output_signal, sr)



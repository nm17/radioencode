import numpy as np
import morseencode


class Morse:
    def gen_wave(self, pos: int, volume: float = 0.5):
        return self._dtype(
            32767 * volume * np.cos(self._frequency * np.pi * pos / self._sample_rate))

    def __init__(self, wps: int = 24, samplerate: int = 4000, freq: int = 2000, dtype=np.int16):
        self._frequency = freq
        self._sample_rate = samplerate
        self._dot_length = 1.2 / wps
        self._dtype = dtype

    def encode(self, msg: str):
        msg_encoded = morseencode.encode_to_morse(msg)
        frames = np.array([], dtype=self._dtype)
        spaceduration = {
            ' ': self._dot_length * 3,
            '/': self._dot_length * 7
        }

        wavec = np.array([], dtype=self._dtype)
        for i in range(int(self._dot_length * self._sample_rate)):
            wavec = np.append(wavec, self.gen_wave(i))
        waveclong = np.tile(wavec, 3)
        for char in msg_encoded:
            if char == '.':
                frames = np.append(frames, wavec)
            elif char == '-':
                frames = np.append(frames, waveclong)
            if char not in spaceduration:
                duration = self._dot_length
            else:
                duration = spaceduration[char]

            frames = np.append(frames, np.zeros(int(duration * self._sample_rate), dtype=self._dtype))
        return frames

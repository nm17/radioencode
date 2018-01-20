from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import *
# etc., as needed

from future import standard_library
standard_library.install_aliases()

import numpy as np

import encode


class Morse:
    def _gen_wave(self, volume: float = 0.5) -> np.ndarray:
        arr = np.array([], dtype=self._dtype)
        for t1 in range(int(self._dot_length * self._sample_rate)):
            arr = np.append(arr, 32767 * volume * np.cos(self._frequency * np.pi * t1 / self._sample_rate))
        return arr

    def __init__(self, wps: int = 24, samplerate: int = 4000, freq: int = 2000, dtype: type = np.int16):
        self._frequency = freq
        self._sample_rate = samplerate
        self._dot_length = 1.2 / wps
        self._dtype = dtype
        self.__spaceduration = {
            ' ': self._dot_length * 3,
            '/': self._dot_length * 7
        }

    def encode(self, msg: str) -> np.ndarray:
        msg_encoded = encode.encode_to_morse(msg)
        frames = np.array([], dtype=self._dtype)

        wavec = self._gen_wave()
        waveclong = np.tile(wavec, 3)
        for char in msg_encoded:
            if char == '.':
                frames = np.append(frames, wavec)
            elif char == '-':
                frames = np.append(frames, waveclong)
            if char not in self.__spaceduration:
                duration = self._dot_length
            else:
                duration = self.__spaceduration[char]

            frames = np.append(frames, np.zeros(int(duration * self._sample_rate), dtype=self._dtype))
        return frames

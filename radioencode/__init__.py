import numpy as np
from audiolazy.lazy_synth import fadein, fadeout

try:
    input = raw_input
except NameError:
    pass

morseAlphabet = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    " ": "/",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    "?": "..--..",
    "'": ".----.",
    "-": "-....-",
    "/": "-..-.",
    "@": ".--.-."
}

inverseMorseAlphabet = dict((v, k) for (k, v) in morseAlphabet.items())


def decode_morse(code, position_in_string=0):
    """
    decode a morse code string
    :param code: morse code string
    :param position_in_string: starting point for decoding
    :return: normal text
    """
    if position_in_string < len(code):
        morse_letter = ''
        for key, char in enumerate(code[position_in_string:]):
            if char == ' ':
                position_in_string = key + position_in_string + 1
                letter = inverseMorseAlphabet[morse_letter]
                return letter + decode_morse(code, position_in_string)

            else:
                morse_letter += char
    else:
        raise KeyError('Bad morse char')


# encode a message in morse code
# spaces between words are represented by '/'
def encode_to_morse(message):
    encoded_message = ''
    for char in message:
        encoded_message += morseAlphabet[char.upper()] + ' '
    return encoded_message


class Morse(object):
    def _gen_wave(self):
        def _fadein(x):
            return np.array(list(fadein(x)), dtype=self._dtype)

        def _fadeout(x):
            return np.array(list(fadeout(x)), dtype=self._dtype)

        arr = np.sin(2 * np.pi * self._frequency * np.arange(
            self._dot_length * self._sample_rate) / self._sample_rate)
        arr[:int(self._sample_rate * self._dot_length / 32)] *= \
            _fadein(int(self._sample_rate * self._dot_length / 32))
        arr[len(arr) - int(self._sample_rate * self._dot_length / 32):] *= \
            _fadeout(int(self._sample_rate * self._dot_length / 32))
        return arr

    def __init__(self, wps=24, samplerate=44100, freq=440, dtype=float):
        self._frequency = freq
        self._sample_rate = samplerate
        self._dot_length = 1.2 / wps
        self._dtype = dtype
        self.__spaceduration = {
            ' ': self._dot_length * 3,
            '/': self._dot_length * 7
        }

    def encode(self, msg):
        msg_encoded = encode_to_morse(msg)
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

            frames = np.append(frames,
                               np.zeros(int(duration * self._sample_rate),
                                        dtype=self._dtype))
        return frames


def main():
    play = True
    try:
        import sounddevice as sd
    except ImportError:
        play = False
    except OSError:
        play = False
    import soundfile as sf

    samplerate = 96000
    freq = 8000
    while True:
        req = input('[P]lay{} or [S]ave: '.format(' [X]' if play else ''))
        if req[0].upper() == 'S':
            data = Morse(samplerate=samplerate, freq=freq).encode(
                input('Text to encode> '))
            try:
                sf.write(input('File name: '), data, samplerate)
            except Exception as err:
                print('Error saving file' + str(err))
        elif req[0].upper() == 'P' and play:
            data = Morse(samplerate=samplerate).encode(
                input('Text to encode> '))
            try:
                sd.play(data, samplerate=samplerate, blocking=True)
            except Exception:
                print('Error playing file')
        else:
            print('Stopping...')
            break


if __name__ == '__main__':
    main()

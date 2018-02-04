import numpy as np

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
    "U": "..-",
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


# parse a morse code string positionInString is the starting point for decoding
def decode_morse(code, position_in_string=0):
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
        raise KeyError("Bad morse char")


# encode a message in morse code, spaces between words are represented by '/'
def encode_to_morse(message):
    encoded_message = ''
    for char in message:
        encoded_message += morseAlphabet[char.upper()] + " "
    return encoded_message


class Morse:
    def _gen_wave(self) -> np.ndarray:
        arr = (np.sin(2 * np.pi * np.arange(
            int(self._dot_length * self._sample_rate)) * self._frequency / self._sample_rate)).astype(self._dtype)
        return arr

    def __init__(self, wps: int = 24, samplerate: int = 48000, freq: int = 1000, dtype: type = np.float32):
        self._frequency = freq
        self._sample_rate = samplerate
        self._dot_length = 1.2 / wps
        self._dtype = dtype
        self.__spaceduration = {
            ' ': self._dot_length * 3,
            '/': self._dot_length * 7
        }

    def encode(self, msg: str) -> np.ndarray:
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

            frames = np.append(frames, np.zeros(int(duration * self._sample_rate), dtype=self._dtype))
        return frames


def main():
    import sounddevice as sd
    import soundfile as sf

    samplerate = 48000
    while True:
        req = input('[P]lay or [S]ave: ')
        if req.upper() == 'S':
            data = Morse(samplerate=samplerate).encode(input('Text to encode> '))
            try:
                sf.write(input('File name: '), data, samplerate)
            except Exception as err:
                print('Error saving file: {}'.format(err), 'red')
        elif req.upper() == 'P':
            data = Morse(samplerate=samplerate).encode(input('Text to encode> '))
            try:
                sd.play(data, samplerate=samplerate, blocking=True)
            except Exception as err:
                print('Error playing file: {}'.format(err))
        else:
            print('Stopping...')
            break

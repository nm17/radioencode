import numpy

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
    "@": ".--.-.",
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
    encoded_message = ""
    for char in message:
        encoded_message += morseAlphabet[char.upper()] + " "
    return encoded_message


class Morse:
    def gen_wave(self, pos: int, volume: float = 0.5):
        return self._dtype(
            32767.0 * volume * numpy.cos(self._frequency * numpy.pi * pos / self._sample_rate))

    def __init__(self, wps: int = 24, samplerate: int = 4000, freq: int = 2000, dtype=numpy.int16):
        self._frequency = freq
        self._sample_rate = samplerate
        self._dot_length = 1.2 / wps
        self._dtype = dtype

    def encode(self, msg: str):
        msg_encoded = encode_to_morse(msg)
        frames = numpy.array([], dtype=self._dtype)
        spaceduration = {
            ' ': self._dot_length * 3,
            '/': self._dot_length * 7
        }

        wavec = numpy.array([], dtype=self._dtype)
        for i in range(int(self._dot_length * self._sample_rate)):
            wavec = numpy.append(wavec, self.gen_wave(i))

        for char in msg_encoded:
            if char == '.':
                frames = numpy.append(frames, wavec)
            elif char == '-':
                frames = numpy.append(frames, numpy.tile(wavec, 3))
            if char not in spaceduration:
                duration = self._dot_length
            else:
                duration = spaceduration[char]

            frames = numpy.append(frames, numpy.zeros(int(duration * self._sample_rate), dtype=self._dtype))
        return frames

import math
import struct

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
    "=": "-...-"
}

inverseMorseAlphabet = dict((v, k) for (k, v) in morseAlphabet.items())


# parse a morse code string positionInString is the starting point for decoding
def decode_morse(code, positionInString=0):
    if positionInString < len(code):
        morseLetter = ""
        for key, char in enumerate(code[positionInString:]):
            if char == " ":
                positionInString = key + positionInString + 1
                letter = inverseMorseAlphabet[morseLetter]
                return letter + decode_morse(code, positionInString)

            else:
                morseLetter += char
    else:
        return ""


# encode a message in morse code, spaces between words are represented by '/'
def encode_to_morse(message):
    encodedMessage = ""
    for char in message[:]:
        encodedMessage += morseAlphabet[char.upper()] + " "
    return encodedMessage


class MorseEngine:
    def gen_wave(self, pos: int):
        return int(32767.0 * math.cos(self._frequency * math.pi * float(pos) / float(self._sample_rate)))

    def __init__(self, wps=24, samplerate=4000.0, freq=2000.0):
        self._frequency = freq
        self._sample_rate = samplerate
        self._dot_length = 1.2 / wps

    def encode(self, msg):
        msg_encoded = encode_to_morse(msg).rstrip(' ')
        frames = bytearray([])
        spaceduration = {
            ' ': self._dot_length * 3,
            '/': self._dot_length * 7
        }

        for char in msg_encoded:
            if char == '.':
                for i in range(int(self._dot_length * self._sample_rate)):
                    frames.extend(struct.pack('h', self.gen_wave(i)))
            elif char == '-':
                for i in range(int(self._dot_length * 3 * self._sample_rate)):
                    frames.extend(struct.pack('h', self.gen_wave(i)))
            if char not in spaceduration:
                duration = self._dot_length
            else:
                duration = spaceduration[char]

            for i in range(int(duration * self._sample_rate)):
                frames.extend(struct.pack('h', 0))
        return frames

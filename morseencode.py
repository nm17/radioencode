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
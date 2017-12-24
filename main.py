import numpy
import sounddevice as sd

import morse

samplerate = 48000
req = input('[L]oad, [P]lay or [S]ave> ')
if req.upper() == 'L':
    sd.play(numpy.load(input('File name> '))['arr_0'], samplerate=samplerate, blocking=True)
elif req.upper() == 'S':
    data = morse.Morse(samplerate=48000).encode(input('Text to encode> '))
    numpy.savez_compressed(input('File name> '), data)
elif req.upper() == 'P':
    data = morse.Morse(samplerate=48000).encode(input('Text to encode> '))
    sd.play(data, samplerate=samplerate, blocking=True)

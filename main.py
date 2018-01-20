from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# noinspection PyCompatibility
from builtins import *
# etc., as needed

from future import standard_library
standard_library.install_aliases()

try:
    import sounddevice as sd
except ImportError:
    play = False
else:
    play = True

try:
    import soundfile as sf
except ImportError:
    save = False
else:
    save = True

try:
    import termcolor
except ImportError:
    coloroutput = False
else:
    coloroutput = True

import audio


def printcolor(text, *args):
    if coloroutput:
        print(termcolor.colored(text, *args))
    else:
        print(text)


samplerate = 48000
while True:
    req = input('[P]lay{} or [S]ave{}: '.format('' if play else ' (unavailable)', '' if save else ' (unavailable)'))
    if req.upper() == 'S' and save:
        data = audio.Morse(samplerate=samplerate).encode(input('Text to encode> '))
        try:
            sf.write(input('File name: '), data, samplerate)
        except Exception as err:
            printcolor('Error saving file: {}'.format(err), 'red')
    elif req.upper() == 'P' and play:
        data = audio.Morse(samplerate=samplerate).encode(input('Text to encode> '))
        try:
            sd.play(data, samplerate=samplerate, blocking=True)
        except Exception as err:
            print('Error playing file: {}'.format(err))
    else:
        print('Stopping...')
        break

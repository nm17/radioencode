import base64
import wave

import morseengine

if __name__ == "__main__":
    samplerate = 4000.0
    file = wave.open('out.wav', 'wb')
    file.setnchannels(1)  # mono
    file.setsampwidth(2)
    file.setframerate(samplerate)
    file.writeframes(morseengine.MorseEngine(samplerate=samplerate).encode(base64.b64encode(b'paris').decode()))
    file.close()

import wavio as wv
import sounddevice as sd
import tempfile
import base64

def write_audio(tempo: int = 2,obj = []):
    temp = tempfile.NamedTemporaryFile(delete=False)
    freq = 44100
    print("Vamos começar  a gravar")
    recording = sd.rec(int(tempo * freq), samplerate=freq, channels=1)
    sd.wait()
    obj["text"] = "Hummm..."
    wv.write(temp.name, recording, freq, sampwidth=2)
    print(temp.name)
    return encode_audio(temp)

def encode_audio(temp):
    audio_content = temp.read()
    base64_audio = base64.b64encode(audio_content)
    encoded_string = base64_audio.decode("utf-8")
    return encoded_string

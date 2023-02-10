import wave
import pyaudio
import config


def executar_audio_gerado():
    chunk = 1024
    f = wave.open(config.URI_SYSTEM + r"\audio.wav", "rb")

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(chunk)

    while data:
        stream.write(data)
        data = f.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()


def identificar_resposta(texto):
    global respostas
    # tratar o texto
    texto = str(texto).lower()
    for resposta in respostas:
        if resposta["nome"] in texto:
            return {"finalizar": True, "resposta": resposta["resposta"]}
    return {"finalizar": False, "resposta": "Desculpe eu não entendi, você pode repetir por favor?"}

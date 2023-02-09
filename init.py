from google.cloud import speech
from google.cloud import storage
import google.cloud.texttospeech as tts
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import base64
import tempfile
import os
import wave
import pyaudio

bucket_name = "teste-aula-plat-formas123"
projeto_name = "assistente_virtual"

def write_audio(tempo: int = 2):
    temp = tempfile.NamedTemporaryFile(delete=False)
    freq = 44100
    print("Vamos começar  a gravar")
    recording = sd.rec(int(tempo * freq), samplerate=freq, channels=1)
    sd.wait()
    wv.write(temp.name, recording, freq, sampwidth=2)
    print(temp.name)
    return encode_audio(temp)


"""
def save_file_in_bucket (){
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(projeto_name + "/" + nome_arquivo)
    blob.upload_from_filename(nome_arquivo)
    return "gs://" + bucket_name + "/" + projeto_name + "/" + nome_arquivo
}
"""

client = speech.SpeechClient()


def encode_audio(temp):
    audio_content = temp.read()
    base64_audio = base64.b64encode(audio_content)
    encoded_string = base64_audio.decode("utf-8")
    return encoded_string

def transcribe_speech(audio_base64: str):
    audio = speech.RecognitionAudio(content=audio_base64)

    config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
      sample_rate_hertz=44100,
      language_code="pt-BR",
      audio_channel_count = 1
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        return result.alternatives[0].transcript
def text_to_wav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = f"audio.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')

def executar_audio_gerado():

    chunk = 1024
    f = wave.open(r"audio.wav","rb")

    p = pyaudio.PyAudio()

    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    output = True)
    data = f.readframes(chunk)

    while data:
        stream.write(data)
        data = f.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Se precisar alterar a voz, essa função lista todas as disponíveis
def list_voices(language_code=None):
    client = tts.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

def identificar_resposta(texto):
    global respostas
    #tratar o texto
    texto = str(texto).lower()
    for resposta in respostas:
        if resposta["nome"] in texto:
            return {"finalizar": True, "resposta": resposta["resposta"]}
    return {"finalizar": False, "resposta": "Desculpe eu não entendi, você pode repetir por favor?"}
#Iniciar conversa

text_to_wav("pt-BR-Neural2-A",
            "Boa tarde Gabriel," # Tudo bem com você? aqui é da imobiliária Casa dos sonhos, em que posso te ajudar? as opções são: Vendas, Aluguel, Administrativo e Financeiro
)
executar_audio_gerado()

respostas = [
    {
        "nome": "vendas",
        "resposta": "Ótimo, vou transferir você para um de nossos corretores de vendas."
    },
    {
        "nome": "aluguel",
        "resposta": "Ótimo, vou transferir você para um de nossos corretores de aluguel."
    },
    {
        "nome": "administrativo",
        "resposta": "Ótimo, vou transferir você para um de nossos administradores."
    },
    {
        "nome": "financeiro",
        "resposta": "Ótimo, vou transferir você para um de nossos contadores."
    },

]

resposta = { "finalizar": False }
while resposta["finalizar"] == False:
    resposta = identificar_resposta(transcribe_speech(write_audio(3)))
    text_to_wav("pt-BR-Neural2-A", resposta["resposta"])
    executar_audio_gerado()

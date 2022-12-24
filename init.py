from google.cloud import speech
from google.cloud import storage
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import base64
import tempfile
import wave 

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
        print("Transcript: {}".format(result.alternatives[0].transcript))

transcribe_speech(write_audio())
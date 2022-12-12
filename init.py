from google.cloud import speech
from google.cloud import storage
import sounddevice as sd 
from scipy.io.wavfile import write 
import wavio as wv
import wave 

bucket_name = "teste-aula-plat-formas123"
projeto_name = "assistente_virtual"

def gravar_audio(nome_arquivo = "recording0.wav",tempo = 5):

  freq = 44100
  recording = sd.rec(int(tempo * freq),  
                    samplerate=freq, channels=1) 
  sd.wait() 
  wv.write(nome_arquivo, recording, freq, sampwidth=2)

  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(projeto_name + "/" + nome_arquivo)
  blob.upload_from_filename(nome_arquivo)
  return "gs://"+bucket_name+"/"+projeto_name+"/"+nome_arquivo


client = speech.SpeechClient()

# The name of the audio file to transcribe

def transcribe_speech(gcs_uri):
  audio = speech.RecognitionAudio(uri=gcs_uri)

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

transcribe_speech(gravar_audio())
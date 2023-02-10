from google.cloud import speech
from google.cloud import storage
import google.cloud.texttospeech as tts
import config

bucket_name = config.BUCKET_NAME
projeto_name = config.PROJECT_NAME

def transcribe_speech(audio_base64: str):
    client = speech.SpeechClient()
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

    filename = config.URI_SYSTEM + r"\audio.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')

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

def save_file_in_bucket () :
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(projeto_name + "/" + nome_arquivo)
    blob.upload_from_filename(nome_arquivo)
    return "gs://" + bucket_name + "/" + projeto_name + "/" + nome_arquivo

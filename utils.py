import os
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech_v1 as texttospeech
from google.oauth2 import service_account
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API desde la variable de entorno
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Validación de la clave de API
if not gemini_api_key:
    raise ValueError("❌ Falta la variable de entorno GEMINI_API_KEY")

# Convertir la clave de API a un formato adecuado para el cliente de Google
credentials = service_account.Credentials.from_service_account_file(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)
client = dialogflow.SessionsClient(credentials=credentials)

# Función para obtener respuesta de Gemini
def get_answer(messages):
    session = client.session_path("your-project-id", "unique-session-id")
    
    # Construir el mensaje de la solicitud
    text_input = dialogflow.TextInput(text=messages, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text
    except Exception as e:
        return f"⚠️ Ocurrió un error al generar la respuesta: {e}"

# Transcripción de voz a texto con Gemini
def speech_to_text(audio_data):
    client = speech.SpeechClient(credentials=credentials)
    
    with open(audio_data, "rb") as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    
    try:
        response = client.recognize(config=config, audio=audio)
        return response.results[0].alternatives[0].transcript
    except Exception as e:
        return f"⚠️ Error en transcripción de audio: {e}"

# Generación de voz a texto con Gemini
def text_to_speech(input_text):
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    
    synthesis_input = texttospeech.SynthesisInput(text=input_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    try:
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        webm_file_path = "temp_audio_play.mp3"
        with open(webm_file_path, "wb") as out:
            out.write(response.audio_content)
        return webm_file_path
    except Exception as e:
        print(f"⚠️ Error en síntesis de voz: {e}")
        return None

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import tempfile
from azure_utils.speech_to_text import transcribe_audio
from azure_utils.translator import translate_text
from azure_utils.clu_predictor import analyze_text_with_clu
from azure_utils.webhook_sender import send_to_webhook
from pydub import AudioSegment

SPEECH_KEY = st.secrets["SPEECH_KEY"]
SPEECH_REGION = st.secrets["SPEECH_REGION"]
TRANSLATOR_KEY = st.secrets["TRANSLATOR_KEY"]
TRANSLATOR_REGION = st.secrets["TRANSLATOR_REGION"]
CLU_KEY = st.secrets["CLU_KEY"]
CLU_ENDPOINT = st.secrets["CLU_ENDPOINT"]
CLU_PROJECT_NAME = st.secrets["CLU_PROJECT_NAME"]
CLU_DEPLOYMENT_NAME = st.secrets["CLU_DEPLOYMENT_NAME"]
WEBHOOK_URL = st.secrets["WEBHOOK_URL"]

def run_voice_reporter():
    st.header("🎙️ Multilingual Voice Reporting")
    st.markdown("Upload or record a voice note in Somali, Urdu, etc. We'll transcribe, translate, and classify it.")

    user_name = st.text_input("Your Name")
    contact_number = st.text_input("Contact Number (optional)")
    uploaded_audio = st.file_uploader("Upload voice note (WAV or MP3)", type=["wav", "mp3"])

    if uploaded_audio and user_name:
        # Determine file type and convert if needed
        # Save uploaded file to a temp file (as WAV PCM)
        if uploaded_audio.type == "audio/mp3" or uploaded_audio.name.lower().endswith(".mp3"):
            # Save MP3 to temp, then convert to WAV PCM
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_tmp:
                mp3_tmp.write(uploaded_audio.read())
                mp3_path = mp3_tmp.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_tmp:
                audio = AudioSegment.from_mp3(mp3_path)
                audio = audio.set_channels(1).set_frame_rate(16000)
                audio.export(wav_tmp.name, format="wav", codec="pcm_s16le")
                temp_audio_path = wav_tmp.name
        else:
            # WAV: Save directly
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_audio.read())
                temp_audio_path = tmp_file.name

        st.audio(uploaded_audio, format="audio/wav")
        st.info("Processing audio...")

        try:
            # 1. Transcribe
            transcribed_text = transcribe_audio(temp_audio_path, SPEECH_KEY, SPEECH_REGION)
            st.success("Transcription:")
            st.write(transcribed_text)

            # 2. Translate
            translated = translate_text(transcribed_text, TRANSLATOR_KEY, TRANSLATOR_REGION)
            st.success("Translation:")
            st.write(translated)

            # 3. CLU Analysis
            intent, entities = analyze_text_with_clu(translated, CLU_KEY, CLU_ENDPOINT, CLU_PROJECT_NAME, CLU_DEPLOYMENT_NAME)
            st.success(f"Detected Category (Intent): {intent}")
            st.write("Extracted Entities:", entities)

            # 4. Send to Power Automate
            payload = {
                "user_name": user_name,
                "category": intent,
                "description": translated,
                "originalLanguage": "auto",
                "location": next((e['text'] for e in entities if e['category'] == 'location'), "unknown"),
                "translated_text": translated,
                "contactNumber": contact_number
            }

            response_code = send_to_webhook(WEBHOOK_URL, payload)
            if response_code == 200:
                st.success("✅ Report submitted to council system via Power Automate!")
            else:
                st.error(f"❌ Failed to send report. HTTP {response_code}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload an audio file and enter your name.")

# If this is the main file, run the app
if __name__ == "__main__":
    st.title("MidlandsBridge - Multilingual Voice Reporting")
    st.markdown("""
    Welcome to MidlandsBridge! This tool helps you report issues to your local council in your native language.
    Just speak, and we'll handle the translation and submission.
    """)
    run_voice_reporter()

# import sys
# import os
# import time
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import tempfile
from azure_utils.speech_to_text import transcribe_audio
from azure_utils.translator import translate_text
from azure_utils.clu_predictor import analyze_text_with_clu
from azure_utils.webhook_sender import send_to_webhook

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

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# import tempfile
# import numpy as np
# import wave
# from streamlit_webrtc import webrtc_streamer, WebRtcMode
# from azure_utils.speech_to_text import transcribe_audio
# from azure_utils.translator import translate_text
# from azure_utils.clu_predictor import analyze_text_with_clu
# from azure_utils.webhook_sender import send_to_webhook

# # Configuration constants
# SPEECH_KEY = "BsE1AWIoIhx6jZKsQmZCesg6uGJXIYIUIDfkLPwYTVrrE0PSN12AJQQJ99BDAC5RqLJXJ3w3AAAYACOGGe8s"
# SPEECH_REGION = "westeurope"
# TRANSLATOR_KEY = "8fV764oHgwzIY9Bl5kaKWFWvXEZqMCrlRFegvW2EhG2qxX6ZtiA8JQQJ99BDAC5RqLJXJ3w3AAAbACOGaHSM"
# TRANSLATOR_REGION = "westeurope"
# CLU_KEY = "DoH8MHyqCbeAzbMYhBWv1KuAyk4eDmYIqYHEUJnhwXeEKMZoyzGwJQQJ99BDAC5RqLJXJ3w3AAAaACOGk9AI"
# CLU_ENDPOINT = "https://midlandbridgelanguage.cognitiveservices.azure.com/"
# CLU_PROJECT_NAME = "MidlandsBridgeCLU"
# CLU_DEPLOYMENT_NAME = "MidlandsBridgeDeployment"
# WEBHOOK_URL = "https://prod-161.westeurope.logic.azure.com:443/workflows/96bfefd76ad3498fbc1baaf49b204f70/triggers/manual/paths/invoke?api-version=2016-06-01"

# class AudioProcessor:
#     def __init__(self):
#         self.frames = []

#     def recv(self, frame):
#         audio = frame.to_ndarray()
#         self.frames.append(audio)
#         return frame

# def run_voice_reporter():
#     st.header("🎤 Multilingual Voice Reporting")
#     st.markdown("Speak in your native language (e.g., Somali, Urdu). We'll transcribe, translate, and classify it.")

#     user_name = st.text_input("Your Name")
#     contact_number = st.text_input("Contact Number (optional)")

#     # Updated webrtc_streamer configuration
#     # Instead of using ClientSettings, we directly pass the configuration options
#     webrtc_ctx = webrtc_streamer(
#         key="voice",
#         mode=WebRtcMode.SENDRECV,
#         rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
#         media_stream_constraints={"audio": True, "video": False},
#         audio_receiver_size=1024,
#         video_processor_factory=None,
#         audio_processor_factory=AudioProcessor,
#     )

#     if webrtc_ctx.audio_receiver and user_name:
#         print("Recording audio...")
#         audio_frames = []
#         try:
#             while True:
#                 frame = webrtc_ctx.audio_receiver.get_frames(timeout=1)[0]
#                 audio_frames.append(frame.to_ndarray())
#         except:
#             pass

#         if audio_frames:
#             audio_data = np.concatenate(audio_frames)
#             audio_data = (audio_data * 32767).astype(np.int16)

#             with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
#                 wf = wave.open(tmp.name, 'wb')
#                 wf.setnchannels(1)
#                 wf.setsampwidth(2)
#                 wf.setframerate(48000)
#                 wf.writeframes(audio_data.tobytes())
#                 wf.close()
#                 temp_audio_path = tmp.name

#                 st.audio(temp_audio_path)
#                 st.info("🔁 Processing recorded audio...")

#                 try:
#                     transcribed_text = transcribe_audio(temp_audio_path, SPEECH_KEY, SPEECH_REGION)
#                     st.success("📝 Transcription:")
#                     st.write(transcribed_text)

#                     translated = translate_text(transcribed_text, TRANSLATOR_KEY, TRANSLATOR_REGION)
#                     st.success("🌍 Translation:")
#                     st.write(translated)

#                     intent, entities = analyze_text_with_clu(translated, CLU_KEY, CLU_ENDPOINT, CLU_PROJECT_NAME, CLU_DEPLOYMENT_NAME)
#                     st.success(f"🎯 Detected Category: {intent}")
#                     st.write("📍 Entities:", entities)

#                     payload = {
#                         "user_name": user_name,
#                         "category": intent,
#                         "description": translated,
#                         "originalLanguage": "auto",
#                         "location": next((e['text'] for e in entities if e['category'] == 'location'), "unknown"),
#                         "translated_text": translated,
#                         "contactNumber": contact_number
#                     }

#                     response_code = send_to_webhook(WEBHOOK_URL, payload)
#                     if response_code == 200:
#                         st.success("✅ Report submitted successfully!")
#                     else:
#                         st.error(f"❌ Failed to send report. HTTP {response_code}")

#                 except Exception as e:
#                     st.error(f"⚠️ Error: {str(e)}")
#     else:
#         st.warning("Please record your message and enter your name to proceed.")

# # If this is the main file, run the app
# if __name__ == "__main__":
#     st.title("MidlandsBridge - Multilingual Voice Reporting")
#     st.markdown("""
#     Welcome to MidlandsBridge! This tool helps you report issues to your local council in your native language.
#     Just speak, and we'll handle the translation and submission.
#     """)
#     run_voice_reporter()


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# import tempfile
# from azure_utils.speech_to_text import transcribe_audio
# from azure_utils.translator import translate_text
# from azure_utils.clu_predictor import analyze_text_with_clu
# from azure_utils.webhook_sender import send_to_webhook

# # Configuration constants
# SPEECH_KEY = "BsE1AWIoIhx6jZKsQmZCesg6uGJXIYIUIDfkLPwYTVrrE0PSN12AJQQJ99BDAC5RqLJXJ3w3AAAYACOGGe8s"
# SPEECH_REGION = "westeurope"
# TRANSLATOR_KEY = "8fV764oHgwzIY9Bl5kaKWFWvXEZqMCrlRFegvW2EhG2qxX6ZtiA8JQQJ99BDAC5RqLJXJ3w3AAAbACOGaHSM"
# TRANSLATOR_REGION = "westeurope"
# CLU_KEY = "DoH8MHyqCbeAzbMYhBWv1KuAyk4eDmYIqYHEUJnhwXeEKMZoyzGwJQQJ99BDAC5RqLJXJ3w3AAAaACOGk9AI"
# CLU_ENDPOINT = "https://midlandbridgelanguage.cognitiveservices.azure.com/"
# CLU_PROJECT_NAME = "MidlandsBridgeCLU"
# CLU_DEPLOYMENT_NAME = "MidlandsBridgeDeployment"
# WEBHOOK_URL = "https://prod-161.westeurope.logic.azure.com:443/workflows/96bfefd76ad3498fbc1baaf49b204f70/triggers/manual/paths/invoke?api-version=2016-06-01"

# def run_voice_reporter():
#     st.header("🎤 Multilingual Voice Reporting")
#     st.markdown("Speak in your native language (e.g., Somali, Urdu). We'll transcribe, translate, and classify it.")

#     user_name = st.text_input("Your Name")
#     contact_number = st.text_input("Contact Number (optional)")

#     # Using file uploader for audio files
#     st.write("### Upload your voice recording")
#     st.write("Record your message using your phone or any recording app, then upload the audio file here.")
    
#     uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a', 'ogg'])

#     if uploaded_file is not None:
#         # Display the uploaded audio for playback
#         st.success("✅ Audio file uploaded successfully!")
#         st.audio(uploaded_file)
        
#         # Save the audio to a temporary file for processing
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
#             tmp.write(uploaded_file.getvalue())
#             temp_audio_path = tmp.name
        
#         if user_name:
#             process_col1, process_col2 = st.columns(2)
#             with process_col1:
#                 process_button = st.button("Process Recording")
#             with process_col2:
#                 reset_button = st.button("Upload Different File")
                
#             if reset_button:
#                 st.experimental_rerun()
                
#             if process_button:
#                 st.info("🔁 Processing audio file...")
                
#                 try:
#                     # Call Azure services to process the audio
#                     transcribed_text = transcribe_audio(temp_audio_path, SPEECH_KEY, SPEECH_REGION)
#                     st.success("📝 Transcription:")
#                     st.write(transcribed_text)

#                     translated = translate_text(transcribed_text, TRANSLATOR_KEY, TRANSLATOR_REGION)
#                     st.success("🌍 Translation:")
#                     st.write(translated)

#                     intent, entities = analyze_text_with_clu(translated, CLU_KEY, CLU_ENDPOINT, CLU_PROJECT_NAME, CLU_DEPLOYMENT_NAME)
#                     st.success(f"🎯 Detected Category: {intent}")
#                     st.write("📍 Entities:", entities)

#                     payload = {
#                         "user_name": user_name,
#                         "category": intent,
#                         "description": translated,
#                         "originalLanguage": "auto",
#                         "location": next((e['text'] for e in entities if e['category'] == 'location'), "unknown"),
#                         "translated_text": translated,
#                         "contactNumber": contact_number
#                     }

#                     response_code = send_to_webhook(WEBHOOK_URL, payload)
#                     if response_code == 200:
#                         st.success("✅ Report submitted successfully!")
#                     else:
#                         st.error(f"❌ Failed to send report. HTTP {response_code}")

#                 except Exception as e:
#                     st.error(f"⚠️ Error: {str(e)}")
#                     import traceback
#                     st.error(f"Error details: {traceback.format_exc()}")
#         else:
#             st.warning("Please enter your name to process the recording.")
#     else:
#         st.info("👆 Upload your audio file using the file uploader above")

#     # Alternative instructions
#     st.markdown("---")
#     st.subheader("Having trouble recording?")
#     st.markdown("""
#     If you're having trouble uploading an audio file, you can:
    
#     1. Use your phone's voice recorder app to record a message
#     2. Email the recording to yourself
#     3. Download it to your computer
#     4. Upload it here
    
#     Alternatively, you can call our phone service at: [phone number]
#     """)

# # If this is the main file, run the app
# if __name__ == "__main__":
#     st.title("MidlandsBridge - Multilingual Voice Reporting")
#     st.markdown("""
#     Welcome to MidlandsBridge! This tool helps you report issues to your local council in your native language.
#     Just upload a voice recording, and we'll handle the translation and submission.
#     """)
    
#     run_voice_reporter()

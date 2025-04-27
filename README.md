# MidlandsBridge Multilingual Voice Reporter

[![Azure](https://img.shields.io/badge/Built%20with-Azure-blue?logo=microsoft-azure)](https://azure.microsoft.com/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Seamless voice reporting for everyone — powered by Microsoft Azure**


MidlandsBridge is an inclusive, AI-powered civic reporting tool that allows users to **record voice messages in any language** (Somali, Urdu, Arabic, etc.) and automatically:

- 🎙️ Transcribes the voice note
- 🌐 Detects the language and translates it to English
- 🧠 Uses Azure CLU to classify the issue (intent + entities)
- 📤 Sends the report to the council system via Power Automate

---

## 🚀 Features
- ✅ In-browser audio recording (no file upload needed)
- 🧠 Azure Speech-to-Text integration
- 🌍 Azure Translator with automatic language detection
- 📊 Azure CLU (Conversational Language Understanding)
- 🔁 Power Automate webhook for instant service ticket generation

---

## ☁️ Azure Services Used

This project integrates several Microsoft Azure services:
- [Azure Speech-to-Text](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/): Voice transcription
- [Azure Translator Text](https://azure.microsoft.com/en-us/services/cognitive-services/translator/): Language detection & translation
- [Azure Language Studio CLU](https://azure.microsoft.com/en-us/services/language-service/conversational-language-understanding/): Intent classification
- [Power Automate](https://flow.microsoft.com/): Automated report forwarding

---

## ⚙️ Azure Setup
1. Create a **Speech service** in Azure → Get `SPEECH_KEY`, `SPEECH_REGION`
2. Create a **Translator Text** service → Get `TRANSLATOR_KEY`, `TRANSLATOR_REGION`
3. Set up a **Language Studio CLU Project** → Publish it and note:
   - `CLU_KEY`, `CLU_ENDPOINT`, `PROJECT_NAME`, `DEPLOYMENT_NAME`
4. Create a **Power Automate flow** with HTTP webhook trigger and copy the **webhook URL**

---

## 🛠 How to Run

### 1. Clone the Repository

```bash
git clone git@github.com:Onyimatics/multilingual_voice_reporter.git
cd multilingual_voice_reporter
```
### 2. (Recommended) Create and activate a virtual environment
```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

### 3. Set Up Your Streamlit Secrets
    
> Before running or deploying the app, create a file at `.streamlit/secrets.toml` and add your Azure and webhook credentials:
 ```toml
 SPEECH_KEY = "your-azure-speech-api-key"
 SPEECH_REGION = "westeurope"

 TRANSLATOR_KEY = "your-azure-translator-key"
 TRANSLATOR_REGION = "westeurope"

 CLU_KEY = "your-azure-clu-key"
 CLU_ENDPOINT = "https://your-clu-endpoint-url"
 CLU_PROJECT_NAME = "your-clu-project"
 CLU_DEPLOYMENT_NAME = "your-clu-deployment"

 WEBHOOK_URL = "https://your-webhook-url"
 ```

 > **Warning:** Do **not** commit `.streamlit/secrets.toml` to version control.  
 > Add this line to your `.gitignore`:
 > ```
 > .streamlit/secrets.toml
 > ```

### 4. Run the Application Locally
 ```bash
 streamlit run streamlit_voice_reporter_final.py
 ```

### 5. Deploying to Streamlit Cloud
 - Push your code to GitHub (excluding any secrets).
 - Go to [share.streamlit.io](https://share.streamlit.io/)
 - Deploy your app from your repository.
 - On the app dashboard, click **"Edit Secrets"**, and copy-paste your `secrets.toml` contents there. Save.

---

## 🔑 Environment Variables & Secrets

This app uses [Streamlit's Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management) for all sensitive keys and URLs to ensure security and seamless deployment both locally and in the cloud.

**Never hardcode credentials in the source code. Always use `st.secrets` to access them, e.g.:**

---

## 📁 Directory Overview
```
midlandsbridge_voice_reporter/
├── app/
│   ├── streamlit_voice_reporter_final.py
│   └── main.py
├── azure_utils/
│   ├── speech_to_text.py
│   ├── translator.py
│   ├── clu_predictor.py
│   └── webhook_sender.py
├── requirements.txt
└── README.md
```

---

## 🏆 Built for Hackathons
This project was developed to address **language accessibility gaps** in local government service delivery and is part of the MidlandsBridge initiative.

> "Let residents speak — we’ll handle the rest."

---

## 📬 License
MIT License

<p align="center">
  <b>Made with ❤️ by Onyinye Favour Ezike</b>
</p>
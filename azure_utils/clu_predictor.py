
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

def analyze_text_with_clu(text, clu_key, clu_endpoint, project_name, deployment_name):
    client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(clu_key))
    result = client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "participantId": "user1",
                    "id": "1",
                    "modality": "text",
                    "language": "en",
                    "text": text
                },
                "isLoggingEnabled": False
            },
            "parameters": {
                "projectName": project_name,
                "deploymentName": deployment_name,
                "verbose": True
            }
        }
    )
    top_intent = result['result']['prediction']['topIntent']
    entities = result['result']['prediction']['entities']
    return top_intent, entities

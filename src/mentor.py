import os
from google import genai
from google.genai import types
from google.genai import errors

def get_mentor_response(user_input, history):
    """
    Gère la communication avec Gemini avec une gestion de quota (429).
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Erreur : Clé API manquante dans le fichier .env"

    client = genai.Client(api_key=api_key)
    
    # On définit l'instruction système
    config = types.GenerateContentConfig(
        system_instruction=(
            "Tu es un Mentor Senior en Data Science et Engineering. "
            "Ton but est d'aider l'utilisateur à réussir ses entretiens techniques. "
            "1. Pose des questions de code (Python/SQL) ou théoriques (ML/Data Eng). "
            "2. Analyse les réponses avec rigueur (Big O, propreté, exactitude). "
            "3. Sois concis pour économiser les tokens."
        ),
        temperature=0.7,
        max_output_tokens=800, # Limite la taille de la réponse pour le quota
    )

    # Optimisation de l'historique : On ne garde que les 6 derniers messages
    # Cela évite que la requête devienne trop lourde (limite de tokens)
    optimized_history = []
    for msg in history[-6:]: 
        role = "model" if msg["role"] == "assistant" else "user"
        optimized_history.append({"role": role, "parts": [{"text": msg["content"]}]})

    try:
        # Création de la session de chat avec l'historique récent
        chat = client.chats.create(
            model="gemini-2.5-flash", # version stable gratuite
            config=config,
            history=optimized_history
        )
        
        # Envoi du message
        response = chat.send_message(user_input)
        return response.text

    except errors.ClientError as e:
        if "429" in str(e):
            return "⚠️ **Quota atteint (Erreur 429)**. Google limite les requêtes gratuites. Attends 1 minute avant de poser la prochaine question."
        return f"❌ Erreur API : {str(e)}"
    except Exception as e:
        return f"❌ Erreur inattendue : {str(e)}"
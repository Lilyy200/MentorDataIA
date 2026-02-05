import re

def clean_code_snippet(text: str) -> str:
    """
    Extrait uniquement le code Python d'une réponse si l'IA 
    a ajouté du texte autour des balises ```python.
    """
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def validate_api_key(api_key: str) -> bool:
    """Vérifie sommairement le format de la clé pour éviter les erreurs inutiles."""
    if not api_key or not api_key.startswith("AIza"):
        return False
    return True
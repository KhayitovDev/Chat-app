import deepl
from decouple import config
# Initialize the DeepL translator using your API key
translator = deepl.Translator(config("DEEPL_KEY"))

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    try:
        result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
        return result.text
    except Exception as e:
        print(f"Error occurred while translating: {str(e)}")
        return text


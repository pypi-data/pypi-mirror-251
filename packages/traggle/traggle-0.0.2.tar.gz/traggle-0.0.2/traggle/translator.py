import requests

class Translator:
    
    @staticmethod
    def translate(to_lang: str, text: str) -> dict:
        result = requests.get(f'http://127.0.0.1:8000/api/translator/translate?to_lang={to_lang}&text={text}').json()
        return result
            
import json
from os import path
from typing import Optional
from config import CONFIG
from logger import logger

SUPPORTED_LANGUAGES = ("en", "pl")


class Translations:
    def __init__(self):
        with open(
            path.join(path.dirname(__file__), "translations.json"), encoding="utf-8"
        ) as f:
            self.translations = json.load(f)
            logger.info(f"Loaded translations. Current language is {CONFIG.language}")

        self.language = CONFIG.language

        # Check if the language is supported
        if self.language not in SUPPORTED_LANGUAGES:
            logger.error(
                f"Unsupported language {self.language}. The only supported ones are: {SUPPORTED_LANGUAGES}"
            )
            exit(-1)

        self.current_translations = self.translations.get(self.language)

    def get_translation(self, key: str, variables: Optional[dict[str, str]]):
        """
        A function to get translation given the key.
        The items from variables will replace every variables in curly braces in the translation value.
        E.g. if the translation value was "Hi {user}" and the variables dict was {'user': 'Arciiix'}, then the output would be "Hi Arciiix"


        Args:
            key (str): The key of the translation
            variables (Optional[dict[str, str]]): The variables to replace in the translation

        """
        translation = self.current_translations.get(key, None)

        if translation is None:
            logger.warning(f"Tried to get a not-existing translation {key}")
            return ""

        # Replace all the variables in curly braces with those from the dictionary
        translation = translation.format(**variables)
        return translation

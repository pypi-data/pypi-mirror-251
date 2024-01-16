class WordNotRecognizedError(Exception):
    """Raised when a request for a specific answer is made to a Reykunyu Entry that has no valid answers."""
    def __init__(self, entry: str):
        super().__init__("\"%s\" has no valid answers." % entry)


class NoPronunciationError(Exception):
    """Raised when a request for a specific pronunciation is made to a Reykunyu Answer that has no pronunciations."""
    def __init__(self, answer: str):
        super().__init__("\"%s\" has no pronunciations." % answer)


class LanguageNotSupportedError(Exception):
    """Raised when an attempt is made to translate a LocalizedText into a language that the text does not support."""
    def __init__(self, word: str, lang_code: str):
        super().__init__("\"%s\" has no translation for language: %s." % (word, lang_code))

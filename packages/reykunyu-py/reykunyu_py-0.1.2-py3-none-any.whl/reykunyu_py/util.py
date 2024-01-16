from reykunyu_py.errors import *


class LocalizedText:
    """Text with multiple translations."""
    def __init__(self, word: str, translations: dict):
        self._word = word
        self._translations = translations
        self._languages = []
        for translation in translations:
            self._languages.append(translation)

    def translate(self, lang_code: str) -> str:
        """Returns the text translated into the given language. Raises a LanguageNotSupported error if the text does not translate to that language."""
        if lang_code in self._translations:
            return self._translations.get(lang_code)
        else:
            raise LanguageNotSupportedError(self._word, lang_code)

    def languages(self) -> list[str]:
        """Returns the list of languages the text translates to."""
        return self._languages


class Pronunciation:
    def __init__(self, data: dict):
        self._syllables = data.get("syllables").split('-')
        self._stressed_index = data.get("stressed") - 1
        self._forest_ipa = data.get("ipa").get("FN")
        self._reef_ipa = data.get("ipa").get("RN")

    def raw(self) -> tuple[list[str], int]:
        """Returns a tuple containing a list of syllables and the index of the stressed syllable"""
        return self._syllables, self._stressed_index

    def get(self, deliminator="-", prefix="", suffix="", capitalized=True):
        """Returns the pronunciation as a string, with each syllable separated by a given deliminator, the stressed syllable optionally surrounded by a given prefix and/or suffix, and the stressed syllable optionally capitalized."""
        syllables = self._syllables
        if capitalized:
            syllables[self._stressed_index] = syllables[self._stressed_index].upper()
        syllables[self._stressed_index] = prefix + syllables[self._stressed_index] + suffix
        return deliminator.join(syllables)

    def ipa(self, dialect: str):
        valid_dialects = ['forest', 'reef']
        if dialect not in valid_dialects:
            raise ValueError("dialect must be one of %r" % valid_dialects)

        if dialect == 'forest':
            return self._forest_ipa
        elif dialect == 'reef':
            return self._reef_ipa


class Answer:
    """A possible meaning and its info for an Entry in a Reykunyu API Response. If an Entry may have multiple meanings it will have multiple Answers."""
    def __init__(self, data: dict):
        self._data = data
        self._translations = []
        for entry in data.get("translations"):
            self._translations.append(LocalizedText(self.root(), entry))
        self._pronunciations = []
        if data.get("pronunciation"):
            for pronunciation in data.get("pronunciation"):
                self._pronunciations.append(Pronunciation(pronunciation))

    def raw(self) -> dict:
        """Returns the raw data of the Answer as a dict."""
        return self._data

    def root(self) -> str:
        """Returns the root word of the answer in Na'vi."""
        return self._data.get("na'vi")

    def translations(self) -> list[dict]:
        """Returns the list of translations."""
        return self.translations()

    def translate(self, lang_code) -> list[str]:
        """Returns all translations of a particular language."""
        translations = []
        for entry in self._translations:
            translations.append(entry.translate(lang_code))

        return translations

    def part_of_speech(self):
        """Returns the part of speech of the word."""
        return self._data.get("type")

    def pronunciations(self):
        """Returns the list of pronunciations of the word."""
        return self._pronunciations

    def best_pronunciation(self):
        """Returns the first pronunciation in the list."""
        if self._pronunciations:
            return self._pronunciations[0]
        else:
            raise NoPronunciationError(self.root())


class Entry:
    """An entry in a Reykunyu API response representing a single word in the input."""
    def __init__(self, data: dict):
        self._data = data
        self._answers = []
        for answer in data.get("sì'eyng"):
            self._answers.append(Answer(answer))
        self._suggestions = data.get("aysämok")

    def raw(self) -> dict:
        """Returns the raw data of the Entry as a dict."""
        return self._data

    def input(self) -> str:
        """Returns the word as it was in the original input."""
        return self._data.get("tìpawm")

    def answers(self) -> list[Answer]:
        """Returns the possible meanings and their info for this Entry."""
        return self._answers

    def best_answer(self) -> Answer:
        """Returns the first Answer for the Entry"""
        if self._answers:
            return self._answers[0]
        else:
            raise WordNotRecognizedError(self.input())

    def suggestions(self) -> list[str]:
        """Returns a list of suggested corrections if the Entry is potentially misspelled."""
        return self._suggestions


class Response:
    """A response from the Reykunyu API for a particular input string."""
    def __init__(self, input_text: str, data: list):
        """Takes in a list response from the Reykunyu API and returns an abstracted Response class."""
        self._data = data
        self._input_text = input_text
        self._entries = []
        for entry in data:
            self._entries.append(Entry(entry))

    def raw(self) -> list:
        """Returns the raw data of the Response as a list."""
        return self._data

    def input(self) -> str:
        """Returns the original input sent to the Reykunyu API."""
        return self._input_text

    def entries(self) -> list[Entry]:
        """Returns every Entry in the Response. Each Entry represents the response for a word in the input."""
        return self._entries

    def entry(self, index: int):
        """Returns the Entry at the specified index."""
        return self._entries[index]

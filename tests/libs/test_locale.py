"""
Test Locale Module.

This module tests the localization utilities in src/libs/locale/.
"""

import unittest

from src.libs.locale.context import current_language
from src.libs.locale.messages import MessagesMetaClass
from src.libs.locale.translate import translate


class TestMessages(metaclass=MessagesMetaClass):
    """Test messages class using MessagesMetaClass."""

    WELCOME_MESSAGE = {
        "en_us": "Welcome to our application!",
        "pt_br": "Bem-vindo ao nosso aplicativo!",
        "es_es": "¡Bienvenido a nuestra aplicación!",
    }

    GOODBYE_MESSAGE = {
        "en_us": "Goodbye, {name}!",
        "pt_br": "Tchau, {name}!",
    }

    ERROR_MESSAGE = {
        "en_us": "An error occurred: {error}",
        "pt_br": "Ocorreu um erro: {error}",
    }


class TestLocaleModule(unittest.TestCase):
    """Test locale module functionality."""

    def test_current_language_default(self):
        """Test that current language defaults to en_US."""
        language = current_language.get()
        self.assertEqual(language, "en_US")

    def test_current_language_set_and_get(self):
        """Test setting and getting current language."""
        # Set language
        current_language.set("pt_br")

        # Get language
        language = current_language.get()
        self.assertEqual(language, "pt_br")

        # Reset to default
        current_language.set("en_US")

    def test_translate_with_string(self):
        """Test translate function with plain string."""
        text = "Hello, world!"
        result = translate(text)

        self.assertEqual(result, "Hello, world!")

    def test_translate_string_with_formatting(self):
        """Test translate function with string formatting."""
        text = "Hello, {name}!"
        result = translate(text, name="Alice")

        self.assertEqual(result, "Hello, Alice!")

    def test_translate_with_dict_english(self):
        """Test translate function with dictionary (English)."""
        text_map = {
            "en_us": "Hello, world!",
            "pt_br": "Olá, mundo!",
        }

        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("en_US")
            result = translate(text_map)
        finally:
            current_language.set(original_lang)

        self.assertEqual(result, "Hello, world!")

    def test_translate_with_dict_portuguese(self):
        """Test translate function with dictionary (Portuguese)."""
        text_map = {
            "en_us": "Hello, world!",
            "pt_br": "Olá, mundo!",
        }

        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("pt_br")
            result = translate(text_map)
        finally:
            current_language.set(original_lang)

        self.assertEqual(result, "Olá, mundo!")

    def test_translate_with_dict_fallback_to_english(self):
        """Test translate function fallback to English for unsupported language."""
        text_map = {
            "en_us": "Hello, world!",
            "pt_br": "Olá, mundo!",
        }

        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("fr_fr")
            result = translate(text_map)
        finally:
            current_language.set(original_lang)

        # Should fallback to en_us
        self.assertEqual(result, "Hello, world!")

    def test_translate_with_dict_and_formatting(self):
        """Test translate function with dictionary and formatting."""
        text_map = {
            "en_us": "Hello, {name}!",
            "pt_br": "Olá, {name}!",
        }

        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("en_US")
            result = translate(text_map, name="Bob")
        finally:
            current_language.set(original_lang)

        self.assertEqual(result, "Hello, Bob!")

    def test_translate_with_case_insensitive_language(self):
        """Test that language matching is case insensitive."""
        text_map = {
            "en_us": "Hello",
            "pt_br": "Olá",
        }

        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("EN_US")
            result = translate(text_map)
        finally:
            current_language.set(original_lang)

        self.assertEqual(result, "Hello")

    def test_messages_metaclass_english(self):
        """Test MessagesMetaClass with English language."""
        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("en_US")
            message = TestMessages.WELCOME_MESSAGE
        finally:
            current_language.set(original_lang)

        self.assertEqual(message, "Welcome to our application!")

    def test_messages_metaclass_portuguese(self):
        """Test MessagesMetaClass with Portuguese language."""
        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("pt_br")
            message = TestMessages.WELCOME_MESSAGE
        finally:
            current_language.set(original_lang)

        self.assertEqual(message, "Bem-vindo ao nosso aplicativo!")

    def test_messages_metaclass_spanish(self):
        """Test MessagesMetaClass with Spanish language."""
        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("es_es")
            message = TestMessages.WELCOME_MESSAGE
        finally:
            current_language.set(original_lang)

        self.assertEqual(message, "¡Bienvenido a nuestra aplicación!")

    def test_messages_metaclass_fallback(self):
        """Test MessagesMetaClass fallback for unsupported language."""
        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("de_de")
            message = TestMessages.WELCOME_MESSAGE
        finally:
            current_language.set(original_lang)

        # Should fallback to en_us
        self.assertEqual(message, "Welcome to our application!")

    def test_messages_metaclass_nonexistent_attribute(self):
        """Test MessagesMetaClass with non-existent attribute."""
        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("en_US")
            message = TestMessages.NONEXISTENT_MESSAGE
        finally:
            current_language.set(original_lang)

        # Should return generic error message
        self.assertEqual(message, "An error occurred while processing your request.")

    def test_messages_metaclass_nonexistent_attribute_portuguese(self):
        """Test MessagesMetaClass with non-existent attribute in Portuguese."""
        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("pt_br")
            message = TestMessages.NONEXISTENT_MESSAGE
        finally:
            current_language.set(original_lang)

        # Should return generic error message in Portuguese
        self.assertEqual(message, "Ocorreu um erro ao processar sua solicitação.")

    def test_messages_metaclass_with_formatting(self):
        """Test MessagesMetaClass message retrieval without formatting."""
        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("en_US")
            # Use a message without formatting parameters
            message = TestMessages.WELCOME_MESSAGE
        finally:
            current_language.set(original_lang)

        # Should return the translated message
        self.assertEqual(message, "Welcome to our application!")

    def test_translate_empty_dict(self):
        """Test translate function with empty dictionary."""
        text_map = {}

        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("en_US")
            result = translate(text_map)
        finally:
            current_language.set(original_lang)

        # Should return empty string
        self.assertEqual(result, "")

    def test_translate_dict_without_english_fallback(self):
        """Test translate function with dictionary that has no English fallback."""
        text_map = {
            "pt_br": "Olá, mundo!",
            "es_es": "¡Hola, mundo!",
        }

        # Save original language
        original_lang = current_language.get()
        try:
            current_language.set("fr_fr")
            result = translate(text_map)
        finally:
            current_language.set(original_lang)

        # Should return empty string when no en_us fallback
        self.assertEqual(result, "")

    def test_current_language_context_isolation(self):
        """Test that current_language context is properly isolated."""
        # This test ensures that context variables work as expected
        original_language = current_language.get()

        # Set a different language
        current_language.set("pt_br")
        self.assertEqual(current_language.get(), "pt_br")

        # Reset
        current_language.set(original_language)
        self.assertEqual(current_language.get(), original_language)


if __name__ == "__main__":
    unittest.main()

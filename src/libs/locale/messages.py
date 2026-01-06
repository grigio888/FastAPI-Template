"""
Locale - Messages - Metaclass.

This module contains the metaclass for the messages.
"""

from typing import ClassVar

from src.libs.locale.enums import LanguageEnum as LE  # noqa: N817
from src.libs.locale.translate import translate as i18n
from src.libs.locale.utils import c_str


class MessagesMetaClass(type):
    """
    # Metaclass for the messages.

    This metaclass allows the messages to be defined in a dictionary format
    with language codes as keys. It functions as a dynamic way to retrieve
    translated messages based on the current language set in the context.

    ## Features:
    - **Dynamic Translation**: Automatically retrieves the translated message
      based on the current language context.
    - **Fallback Mechanism**: If the translation for the current language is not
      available, it defaults to English (`en_us`).

    ---

    ## Usage:

    ```python
    from src.libs.locale.messages import MessagesMetaClass

    class Messages(metaclass=MessagesMetaClass):
        EXAMPLE_MESSAGE: ClassVar[str] = {
            "en_us": "This is an example message.",
            "pt_br": "Esta é uma mensagem de exemplo.",
        }

    # Access the message using the class name.
    print(Messages.EXAMPLE_MESSAGE)
    # ^ Returns the translated message based on the current language.
    ```
    """

    GENERIC_ERROR: ClassVar[str] = c_str({
        LE.en_us: "An error occurred while processing your request.",
        LE.pt_br: "Ocorreu um erro ao processar sua solicitação.",
    })

    def __getattribute__(cls, name: str) -> str:
        """
        Get the message by name.

        This method call the i18n function to translate the message.
        """

        try:
            text = object.__getattribute__(cls, name)

        except AttributeError:
            text = object.__getattribute__(cls, "GENERIC_ERROR")

        return i18n(text)

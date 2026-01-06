"""
Users - Utilities.
"""

from src.libs.fetch import fetch


async def generate_random_name() -> str:
    """
    Generate a random name using an external API.
    """

    word = []

    for _ in range(3):
        _response, json, _error = await fetch(
            "https://random-word-api.herokuapp.com/word",
        )
        word.append(json[0].capitalize())

    return "".join(word)

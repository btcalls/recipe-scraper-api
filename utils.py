"""
List of potentially parsed ingredient names that constitute to an invalid one.

Case 1: Recipe may specify how to serve the dish, and one of the options is to serve it plain, 
hence keywords such as "Nothing", "None", "No", "N/A" are used (seen in https://www.recipetineats.com/crispy-oven-baked-quesadillas/).

List will be expanded as needed.
"""
erroneous_ingredients = ["Nothing", "None", "No", "N/A"]
"""
Words that are not needed in the recipe title or description.

Case 1: Description pinpoints to a video within the recipe page (seen in https://www.recipetineats.com/crispy-oven-baked-quesadillas/).

List will be expanded as needed.
"""
remove_words = ["Recipe video above."]


def cleanup_strip_text(text: str, is_title_case=True):
    """
    Cleans up the text by removing unwanted characters and formatting.

    Returns:
        str: cleaned text.
    """
    text = text \
        .replace('\n', '') \
        .replace('\r', '') \
        .replace('/ ', '') \
        .replace(' /', '') \

    for word in remove_words:
        text = text.replace(word, '')

    text = text.strip()

    return text.title() if is_title_case else text


def cleanup_strip_title(text: str):
    """
    Cleans up the title text by removing unwanted characters and formatting.

    Returns:
        str: cleaned title.
    """
    unwanted_words = ['Recipe', 'Recipes', 'Recipe:', 'Recipes:']
    cleaned = cleanup_strip_text(text, True)

    # Remove any unwanted words from the title (e.g. "Recipe")
    for word in unwanted_words:
        cleaned = cleaned.replace(word, '')

    return cleaned.strip()

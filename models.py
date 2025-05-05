from uuid import uuid4

from ingredient_parser import parse_ingredient


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


def cleanup_strip_text(text: str, is_title=True):
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

    return text.title() if is_title else text


class Recipe():
    def __init__(self, json):
        self.id = str(uuid4())
        self.name = cleanup_strip_text(json['title'])
        self.category = cleanup_strip_text(json['category'])
        self.cuisine = cleanup_strip_text(json['cuisine'])
        self.description = cleanup_strip_text(json['description'], False)
        self.prep_time = json['prep_time']
        self.total_time = json['total_time']
        self.instructions = json['instructions_list']

        # Parse ingredients
        ingredients_list = []

        for item in json['ingredients']:
            ingredient = Ingredient(item)

            if ingredient.name in erroneous_ingredients:
                continue

            ingredients_list.append(ingredient)

        self.ingredients = ingredients_list

    def __str__(self):
        return f"""
        {self.name} - {self.category} - {self.cuisine}
    
        Description: {self.description}
        Prep time: {self.prep_time} mins.
        Total time: {self.total_time} mins.
        """

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "cuisine": self.cuisine,
            "description": self.description,
            "prep_time": self.prep_time,
            "total_time": self.total_time,
            "instructions_list": self.instructions,
            "instance_description": str(self),
            "ingredients": [
                {"name": ingredient.name,
                 "amount": ingredient.amount,
                 "method": ingredient.method,
                 "instance_description": str(ingredient)}
                for ingredient in self.ingredients
            ]
        }


class Ingredient():
    def __init__(self, name):
        self._ingredient = parse_ingredient(name)

        self.name = cleanup_strip_text(self._ingredient.name[0].text, False)
        self.amount = None
        self.method = None

        if self._ingredient.amount is not None and len(self._ingredient.amount) > 0:
            self.amount = cleanup_strip_text(
                self._ingredient.amount[0].text, False)

        if self._ingredient.preparation is not None:
            self.method = cleanup_strip_text(
                self._ingredient.preparation.text, False) \
                .replace('(', '') \
                .replace(')', '') \


    def __str__(self):
        if self.amount is None and self.method is None:
            return self.name
        elif self.amount is None:
            return f"{self.name} ({self.method})"
        elif self.method is None:
            return f"{self.amount} {self.name}"
        else:
            return f"{self.amount} {self.name} ({self.method})"

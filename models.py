from ingredient_parser import parse_ingredient


class Recipe():
    def __init__(self, json):
        self.name = json['title']
        self.category = json['category']
        self.cuisine = json['cuisine']
        self.description = json['description']
        self.prep_time = json['prep_time']
        self.total_time = json['total_time']
        self.instructions = json['instructions_list']

        # Parse ingredients
        ingredients_list = []

        for ingredient in json['ingredients']:
            ingredients_list.append(Ingredient(ingredient))

        self.ingredients = ingredients_list

    def __str__(self):
        return f"""
        {self.name} - {self.category} - {self.cuisine}
    
        Description: {self.description}
        Prep time: {self.prep_time} mins.
        Total time: {self.total_time} mins.
        """


class Ingredient():
    def __init__(self, name):
        self._ingredient = parse_ingredient(name)

        self.name = self._ingredient.name[0].text
        self.amount = None
        self.method = None

        if self._ingredient.amount is not None and len(self._ingredient.amount) > 0:
            self.amount = self._ingredient.amount[0].text

        if self._ingredient.preparation is not None:
            self.method = self._ingredient.preparation.text

    def __str__(self):
        if self.amount is None and self.method is None:
            return self.name
        elif self.amount is None:
            return f"{self.name}, {self.method}"
        elif self.method is None:
            return f"{self.amount} {self.name}"
        else:
            return f"{self.amount} {self.name}, {self.method}"

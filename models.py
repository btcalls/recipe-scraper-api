from uuid import uuid4

from ingredient_parser import parse_ingredient

from utils import cleanup_strip_text, cleanup_strip_title, erroneous_ingredients


class Recipe():
    def __init__(self, json):
        self.id = str(uuid4())
        self.name = cleanup_strip_title(json['title'])
        self.author = cleanup_strip_text(json['author'], False)
        self.site_name = cleanup_strip_text(json['site_name'], False)
        self.image = json['image']
        self.categories = cleanup_strip_text(json['category']).split(',')
        self.cuisines = cleanup_strip_text(json['cuisine']).split(',')
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
        {self.name} - {",".join(self.categories)} - {",".join(self.cuisines)}
    
        Description: {self.description}
        Prep time: {self.prep_time} mins.
        Total time: {self.total_time} mins.
        """

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": {
                "name": self.author,
                "website": self.site_name,
            },
            "image_url": self.image,
            "categories": self.categories,
            "cuisines": self.cuisines,
            "description": self.description,
            "prep_time": self.prep_time,
            "total_time": self.total_time,
            "instructions": self.instructions,
            "instance_description": str(self),
            "ingredients": [item.to_dict() for item in self.ingredients]
        }


class Ingredient():
    def __init__(self, name):
        _ingredient = parse_ingredient(name)

        self.name = cleanup_strip_text(_ingredient.name[0].text, False).lower()
        self.amount = None
        self.method = None

        if _ingredient.amount is not None and len(_ingredient.amount) > 0:
            self.amount = cleanup_strip_text(
                _ingredient.amount[0].text, False)

        if _ingredient.preparation is not None:
            self.method = cleanup_strip_text(
                _ingredient.preparation.text, False) \
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

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "method": self.method,
            "instance_description": str(self)
        }

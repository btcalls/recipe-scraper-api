
from recipe_scrapers import scrape_html, scrape_me
from urllib.request import Request, urlopen

from models import Recipe


def fetch_html(url):
    """
    Fetches the HTML content of a webpage. Typically used for `recipe_scrapers` unsupported websites.

    Returns:
        str: decoded HTML content of the webpage.
    """
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(request)
    data = response.read()

    return data.decode('utf-8')


def parse_recipe(url):
    """
    Parses a recipe from a given URL.

    Returns:
        Recipe: object containing key information. 
    """
    recipe = None

    try:
        # * Default scraper
        scraper = scrape_me(url)
        recipe = Recipe(scraper.to_json())
    except Exception as e:
        # * Handle unsupported websites
        html = fetch_html(url)
        scraper = scrape_html(html, url, supported_only=False)
        recipe = Recipe(scraper.to_json())

    return recipe


if __name__ == '__main__':
    url = 'https://panlasangpinoy.com/cheesy-baked-macaroni-pinoy-style/'
    recipe = parse_recipe(url)

    print(recipe)

    if recipe is not None:
        for item in recipe.ingredients:
            print(item)

        for item in recipe.instructions:
            print(item)

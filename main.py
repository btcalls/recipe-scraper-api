from fastapi import FastAPI, Body

from utils import parse_recipe


app = FastAPI()


@app.post("/recipe/parse", status_code=201)
async def parse_url(url: str = Body(..., embed=True)):
    recipe = parse_recipe(url)

    return {"name": recipe.name}

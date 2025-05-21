from fastapi import FastAPI, Body, HTTPException

from utils import parse_recipe


app = FastAPI()


@app.post("/recipe/parse", status_code=201)
async def parse_url(url: str = Body(..., embed=True)):
    recipe = parse_recipe(url)

    if recipe is None:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse the recipe at URL: {url}."
        )

    return recipe.to_dict()

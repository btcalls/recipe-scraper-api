from fastapi import FastAPI, Body, HTTPException

from parsers import parse_recipe

app = FastAPI()


@app.post("/recipe/parse", status_code=201)
async def parse_url(url: str = Body(..., embed=True)):
    recipe = parse_recipe(url)

    if recipe is None:
        raise HTTPException(
            status_code=501,
            detail=f"Failed to parse the recipe at {url}. Please check the URL or try a different one."
        )

    return recipe.to_dict()

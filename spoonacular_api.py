import requests
import re
import os

SPOONACULAR_KEY = os.getenv("SPOONACULAR_KEY")

def clean_text(text):
    """Remove HTML tags and trim whitespace."""
    return re.sub('<[^<]+?>', '', text).strip()

def get_recipes(query):
    # Search for recipes by ingredients
    search_url = "https://api.spoonacular.com/recipes/findByIngredients"
    search_params = {
        "ingredients": query,
        "number": 3,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": SPOONACULAR_KEY
    }

    try:
        response = requests.get(search_url, params=search_params)
        basic_recipes = response.json()
    except Exception as e:
        print("Error fetching basic recipes:", e)
        return []
    
    if not isinstance(basic_recipes, list):
        print("Unexpected response format:", basic_recipes)
        return []

    # Fetch full details for each recipe
    detailed = []
    for r in basic_recipes:
        if not isinstance(r, dict) or "id" not in r:
            continue

        recipe_id = r["id"]
        info_url = f"https://api.spoonacular.com/recipes/{r['id']}/information"
        info_params = {"apiKey": SPOONACULAR_KEY}

        try:
            info_response = requests.get(info_url, params=info_params)
            info = info_response.json()
        except Exception as e:
            print(f"Error fetching details for recipe {recipe_id}:", e)
            continue
        
        # Ingredients with measurements
        ingredients = [
            clean_text(f"{i.get('amount', '')} {i.get('unit', '')} {i.get('name', '')}")
            for i in info.get("extendedIngredients", [])
        ]

         # Extract steps
        steps = []
        instructions = info.get("analyzedInstructions", [])
        if instructions and instructions[0].get("steps"):
            steps = [clean_text(step["step"]) for step in instructions[0]["steps"]]

        # Extract calories
        nutrition = info.get("nutrition", {}).get("nutrients", [])
        calories = next((n["amount"] for n in nutrition if n["name"] == "Calories"), "N/A")


        detailed.append({
            "title": clean_text(info.get("title", "Untitled")),
            "ingredients": ingredients,
            "steps": steps,
            "readyInMinutes": info.get("readyInMinutes", "N/A"),
            "calories": calories
            
        })

    return detailed


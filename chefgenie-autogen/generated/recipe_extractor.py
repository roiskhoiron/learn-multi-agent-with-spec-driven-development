import re
from typing import List, Dict, Any


def extract_recipe(raw_text: str) -> Dict[str, Any]:
    """
    Extracts recipe name, ingredients, and instructions from a raw recipe text.

    Args:
        raw_text (str): Raw recipe text or URL content.

    Returns:
        dict: A dictionary containing the title, ingredients list, and instructions list.
              - title (str): The name of the recipe.
              - ingredients (list): A list of dictionaries with keys 'name', 'quantity', and 'unit'.
              - instructions (list): A list of strings representing the steps.
    """
    # 1. Extract Title
    # Assume the first word(s) before the first colon or period is the title.
    # For "Pancakes: Mix...", title is "Pancakes".
    title_match = re.match(r'^([A-Za-z0-9\s]+?)[\s:,.]+', raw_text)
    title = title_match.group(1).strip() if title_match else ""

    # 2. Extract Ingredients
    # Pattern for ingredients: number + unit + name, or number + name (if unit is implied or missing)
    # Examples from test case: "1 cup flour", "1 egg" (unit count), "1 cup milk"
    ingredient_pattern = r'(\d+(?:\.\d+)?)\s*(cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|egg|eggs|count)?\s*([a-zA-Z]+)'
    ingredient_matches = re.finditer(ingredient_pattern, raw_text)

    ingredients = []
    for match in ingredient_matches:
        quantity_str = match.group(1)
        unit_raw = match.group(2) if match.group(2) else "count"
        name = match.group(3)

        # Normalize unit to singular form as per expected output style, or keep as is if specific
        # Map common plural units to singular for consistency with test case expectation
        unit_map = {
            "cups": "cup",
            "tablespoons": "tablespoon",
            "teaspoons": "teaspoon",
            "eggs": "egg"
        }
        unit = unit_map.get(unit_raw, unit_raw)

        ingredients.append({
            "name": name,
            "quantity": float(quantity_str) if '.' in quantity_str else int(quantity_str),
            "unit": unit
        })

    # 3. Extract Instructions
    # Instructions are typically sentences following the ingredients.
    # We split the remaining text after the title/ingredients section into sentences.
    # A simple heuristic: Split by period followed by space or end of string.
    # Remove the title part first to get the body.
    body_text = raw_text[len(title):].strip()
    
    # Split instructions by period, ignoring the ingredient numbers which might have periods if decimals (though rare in this context)
    # More robust: Split by ". " or "." at end of string.
    instructions_raw = re.split(r'\.\s*', body_text)
    
    # Clean up instructions: remove empty strings and strip whitespace
    instructions = [instr.strip() for instr in instructions_raw if instr.strip()]

    return {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions
    }
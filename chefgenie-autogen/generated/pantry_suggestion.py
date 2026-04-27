from typing import List, Dict, Any


def suggest_recipes(pantry: List[Dict[str, Any]], recipe_database: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Suggests recipes based on available pantry items and identifies missing ingredients.

    Args:
        pantry (List[Dict]): A list of dictionaries representing available pantry items.
            Each dictionary has keys 'name' (str), 'quantity' (number), and 'unit' (str).
        recipe_database (List[Dict]): A list of dictionaries representing the recipe database.
            Each dictionary has keys 'title' (str) and 'ingredients' (List[Dict]).
            The 'ingredients' key contains a list of dictionaries with keys 'name', 'quantity', and 'unit'.

    Returns:
        List[Dict]: A list of suggested recipes, each represented by a dictionary with keys:
            - 'recipe_title' (str): The title of the recipe.
            - 'match_score' (number): A score indicating how well the pantry items match the recipe ingredients.
            - 'missing_ingredients' (List[Dict]): A list of missing ingredients required for the recipe, 
              each with keys 'name', 'quantity', and 'unit'.
    """

    def calculate_match_score(recipe_ingredients: List[Dict], pantry_items: List[Dict]) -> tuple:
        """
        Calculates the match score and identifies missing ingredients between a recipe's ingredients and the pantry items.

        Args:
            recipe_ingredients (List[Dict]): The ingredients required for a specific recipe.
            pantry_items (List[Dict]): The available items in the pantry.

        Returns:
            tuple: A tuple containing:
                - match_score (number): The ratio of matched ingredient quantities to total required quantities.
                - missing_ingredients (List[Dict]): A list of ingredients that are missing or insufficient in the pantry.
        """
        # Create a lookup dictionary for pantry items by name and unit
        pantry_lookup = {
            f"{item['name']}_{item['unit']}": item['quantity']
            for item in pantry_items
        }

        total_required_quantity = 0
        matched_quantity = 0
        missing_ingredients = []

        for ingredient in recipe_ingredients:
            key = f"{ingredient['name']}_{ingredient['unit']}"
            required_qty = ingredient['quantity']
            available_qty = pantry_lookup.get(key, 0)

            total_required_quantity += required_qty

            if available_qty >= required_qty:
                matched_quantity += required_qty
            else:
                # Ingredient is missing or insufficient
                missing_ingredients.append({
                    'name': ingredient['name'],
                    'quantity': required_qty - available_qty,
                    'unit': ingredient['unit']
                })

        # Calculate match score as the ratio of matched quantity to total required quantity
        if total_required_quantity == 0:
            match_score = 1.0
        else:
            match_score = matched_quantity / total_required_quantity

        return match_score, missing_ingredients

    suggestions = []

    for recipe in recipe_database:
        match_score, missing_ingredients = calculate_match_score(
            recipe['ingredients'], pantry
        )
        suggestions.append({
            'recipe_title': recipe['title'],
            'match_score': round(match_score, 2),  # Round to 2 decimal places for readability
            'missing_ingredients': missing_ingredients
        })

    return suggestions
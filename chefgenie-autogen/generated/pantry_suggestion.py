import yaml
from typing import List, Dict, Any


class PantrySuggestion:
    """
    Suggests recipes based on available pantry items and identifies missing ingredients.
    
    Attributes:
        recipe_database (List[Dict[str, Any]]): A list of recipes with their required ingredients.
    """

    def __init__(self, recipe_database: List[Dict[str, Any]]) -> None:
        """
        Initialize the PantrySuggestion class with a recipe database.

        Args:
            recipe_database (List[Dict[str, Any]]): A list of recipes where each recipe is a dictionary 
                containing 'title' and 'ingredients'. Each ingredient is a dictionary with 'name', 'quantity', 
                and 'unit'.
        """
        self.recipe_database = recipe_database

    def suggest_recipes(
        self, pantry: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Suggests recipes based on the available pantry items.

        Args:
            pantry (List[Dict[str, Any]]): A list of pantry items where each item is a dictionary 
                containing 'name', 'quantity', and 'unit'.

        Returns:
            List[Dict[str, Any]]: A list of suggested recipes, each represented as a dictionary with 
                'recipe_title', 'match_score', and 'missing_ingredients'.
        """
        suggestions = []
        
        for recipe in self.recipe_database:
            missing_ingredients = []
            required_total_quantity = 0
            matched_quantity = 0

            for ingredient in recipe["ingredients"]:
                ing_name = ingredient["name"]
                ing_quantity = ingredient["quantity"]
                ing_unit = ingredient["unit"]

                # Find the corresponding pantry item
                pantry_item = next(
                    (item for item in pantry if item["name"] == ing_name),
                    None,
                )

                required_total_quantity += ing_quantity

                if pantry_item:
                    matched_quantity += min(pantry_item["quantity"], ing_quantity)
                else:
                    # If not found, add to missing ingredients
                    missing_ingredients.append(
                        {
                            "name": ing_name,
                            "quantity": ing_quantity,
                            "unit": ing_unit,
                        }
                    )

            # Calculate match score as the ratio of matched quantity to required total quantity
            match_score = (
                matched_quantity / required_total_quantity if required_total_quantity > 0 else 0
            )

            suggestions.append(
                {
                    "recipe_title": recipe["title"],
                    "match_score": round(match_score, 2),
                    "missing_ingredients": missing_ingredients,
                }
            )

        return suggestions


def load_spec_from_yaml(yaml_content: str) -> Dict[str, Any]:
    """
    Load the specification from a YAML string.

    Args:
        yaml_content (str): The YAML content as a string.

    Returns:
        Dict[str, Any]: The parsed specification as a dictionary.
    """
    return yaml.safe_load(yaml_content)


def validate_pantry(pantry: List[Dict[str, Any]]) -> bool:
    """
    Validate the structure of the pantry list.

    Args:
        pantry (List[Dict[str, Any]]): The pantry list to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(pantry, list):
        return False
    
    for item in pantry:
        if not isinstance(item, dict):
            return False
        if "name" not in item or "quantity" not in item or "unit" not in item:
            return False
        if not isinstance(item["name"], str):
            return False
        if not isinstance(item["quantity"], (int, float)):
            return False
        if not isinstance(item["unit"], str):
            return False
            
    return True


def validate_recipe_database(recipe_database: List[Dict[str, Any]]) -> bool:
    """
    Validate the structure of the recipe database.

    Args:
        recipe_database (List[Dict[str, Any]]): The recipe database to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(recipe_database, list):
        return False
    
    for recipe in recipe_database:
        if not isinstance(recipe, dict):
            return False
        if "title" not in recipe or "ingredients" not in recipe:
            return False
        if not isinstance(recipe["title"], str):
            return False
        if not isinstance(recipe["ingredients"], list):
            return False
            
        for ingredient in recipe["ingredients"]:
            if not isinstance(ingredient, dict):
                return False
            if "name" not in ingredient or "quantity" not in ingredient or "unit" not in ingredient:
                return False
            if not isinstance(ingredient["name"], str):
                return False
            if not isinstance(ingredient["quantity"], (int, float)):
                return False
            if not isinstance(ingredient["unit"], str):
                return False
                
    return True


def main() -> None:
    """
    Main function to demonstrate the usage of PantrySuggestion.
    """
    # Example YAML content
    yaml_content = """
    name: PantrySuggestion
    description: Suggests recipes based on available pantry items and identifies missing ingredients.
    version: 1.0.0
    input:
      type: object
      properties:
        pantry:
          type: array
          items:
            type: object
            properties:
              name: {type: string}
              quantity: {type: number}
              unit: {type: string}
        recipe_database:
          type: array
          items:
            type: object
            properties:
              title: {type: string}
              ingredients:
                type: array
                items:
                  type: object
                  properties:
                    name: {type: string}
                    quantity: {type: number}
                    unit: {type: string}
    output:
      type: array
      items:
        type: object
        properties:
          recipe_title: {type: string}
          match_score: {type: number}
          missing_ingredients:
            type: array
            items:
              type: object
              properties:
                name: {type: string}
                quantity: {type: number}
                unit: {type: string}
    """

    # Load specification
    spec = load_spec_from_yaml(yaml_content)
    
    # Example data
    pantry = [
        {"name": "flour", "quantity": 500, "unit": "g"},
        {"name": "sugar", "quantity": 200, "unit": "g"},
        {"name": "butter", "quantity": 100, "unit": "g"},
        {"name": "eggs", "quantity": 4, "unit": "pcs"},
    ]

    recipe_database = [
        {
            "title": "Simple Cake",
            "ingredients": [
                {"name": "flour", "quantity": 200, "unit": "g"},
                {"name": "sugar", "quantity": 150, "unit": "g"},
                {"name": "butter", "quantity": 100, "unit": "g"},
                {"name": "eggs", "quantity": 2, "unit": "pcs"},
            ],
        },
        {
            "title": "Bread",
            "ingredients": [
                {"name": "flour", "quantity": 500, "unit": "g"},
                {"name": "sugar", "quantity": 20, "unit": "g"},
                {"name": "butter", "quantity": 10, "unit": "g"},
                {"name": "eggs", "quantity": 1, "unit": "pcs"},
            ],
        },
        {
            "title": "Cookies",
            "ingredients": [
                {"name": "flour", "quantity": 300, "unit": "g"},
                {"name": "sugar", "quantity": 150, "unit": "g"},
                {"name": "butter", "quantity": 200, "unit": "g"},
                {"name": "eggs", "quantity": 3, "unit": "pcs"},
            ],
        },
    ]

    # Validate inputs
    if not validate_pantry(pantry):
        raise ValueError("Invalid pantry data.")
    
    if not validate_recipe_database(recipe_database):
        raise ValueError("Invalid recipe database.")

    # Create PantrySuggestion instance
    suggestion_engine = PantrySuggestion(recipe_database)

    # Get suggestions
    suggestions = suggestion_engine.suggest_recipes(pantry)

    # Print results
    for suggestion in suggestions:
        print(f"Recipe: {suggestion['recipe_title']}")
        print(f"Match Score: {suggestion['match_score']}")
        print(f"Missing Ingredients: {suggestion['missing_ingredients']}")
        print()


if __name__ == "__main__":
    main()
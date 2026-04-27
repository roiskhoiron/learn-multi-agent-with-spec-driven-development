Generate Python code for the following specification:

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
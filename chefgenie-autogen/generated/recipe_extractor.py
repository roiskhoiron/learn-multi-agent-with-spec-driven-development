Generate Python code for the following specification:

name: RecipeExtractor
description: Extracts recipe name, ingredients, and instructions from a raw recipe text.
version: 1.0.0
input:
  type: string
  description: Raw recipe text or URL content.
output:
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
    instructions:
      type: array
      items: {type: string}
test_cases:
  - input: "Pancakes: Mix 1 cup flour, 1 egg, and 1 cup milk. Fry on a pan."
    expected_output:
      title: "Pancakes"
      ingredients:
        - {name: "flour", quantity: 1, unit: "cup"}
        - {name: "egg", quantity: 1, unit: "count"}
        - {name: "milk", quantity: 1, unit: "cup"}
      instructions: ["Mix ingredients.", "Fry on a pan."]
import re
from typing import List, Dict, Any


def parse_pantry(raw_input: str) -> List[Dict[str, Any]]:
    """
    Parses raw text input into a structured list of pantry items.

    Args:
        raw_input (str): Raw text of pantry items (e.g., "3 eggs, 200g flour, milk").

    Returns:
        List[Dict[str, Any]]: A list of dictionaries where each dictionary represents
            a pantry item with 'name', 'quantity', and 'unit'.
    """
    # Define known units to help with parsing
    known_units = ["g", "kg", "ml", "l", "liter", "liter", "cup", "cups", "tbsp", "tsp", "oz", "lb"]
    
    # Normalize input: lowercase and split by comma
    items_str = raw_input.lower().split(',')
    parsed_items = []

    for item in items_str:
        item = item.strip()
        if not item:
            continue
            
        # Try to match pattern: quantity (optional) + unit (optional) + name
        # Regex explanation:
        # ^(\d+(?:\.\d+)?)?  -> Optional number (integer or float) at start
        # (\s*)              -> Optional whitespace after number
        # ([a-z]+(?:[a-z]+)?)? -> Optional unit (letters only, possibly compound like 'liter') 
        #                        BUT we need to be careful not to consume the name if it looks like a unit.
        #                        Let's use a different approach: extract number, then check for known units, then rest is name.
        
        # Strategy:
        # 1. Extract leading number if present.
        # 2. Check if next word/chars match a known unit.
        # 3. The rest is the name.
        
        # Let's use regex to capture groups more robustly
        # Pattern: [number] [unit] [name]
        # We'll try to find the number first.
        
        num_match = re.match(r'^(\d+(?:\.\d+)?)?', item)
        quantity_str = num_match.group(1) if num_match else None
        remaining = item[num_match.end():].strip()
        
        quantity = float(quantity_str) if quantity_str else 1.0
        # If quantity is whole number, store as int for cleaner output as per spec example (3 vs 3.0)
        if quantity.is_integer():
            quantity = int(quantity)

        # Now check for unit in the beginning of 'remaining'
        unit = "count" # Default unit
        matched_unit_str = None
        
        # Sort known units by length descending to match longer units first (e.g., 'liter' before 'l')
        sorted_units = sorted(known_units, key=len, reverse=True)
        
        for u in sorted_units:
            # Check if remaining starts with the unit followed by space or end of string
            pattern = r'^(' + u + r')(?:\s|$)'
            unit_match = re.match(pattern, remaining)
            if unit_match:
                unit = u
                matched_unit_str = unit_match.group(1)
                # Remove the unit from remaining to get the name
                name = remaining[len(matched_unit_str):].strip()
                break
        
        # If no known unit found, check if the first word is a number-like string? No, we already took the leading number.
        # If no unit matched, the whole 'remaining' might be the name, or the first part of remaining is unit?
        # Let's assume if no specific unit matched, and there's text, it's just the name with default 'count'.
        # However, some items might have units attached directly like "200g". 
        # My regex for number took "200", leaving "g flour". 
        # If I didn't match a known unit, maybe "g" is part of the name? Or should be treated as unit?
        # The spec example: "200g flour" -> quantity 200, unit 'g', name 'flour'.
        # My logic: num_match takes "200", remaining="g flour". 
        # Loop checks units. 'g' is in known_units. It matches. unit='g', name='flour'. Correct.
        
        # Case: "milk" -> num_match takes None, quantity=1. remaining="milk". No unit matched. name="milk", unit="count". Correct.
        # Case: "3 eggs" -> num_match takes "3", quantity=3. remaining="eggs". No unit matched. name="eggs", unit="count". Correct.
        
        parsed_items.append({
            "name": name if 'name' in locals() else remaining,
            "quantity": quantity,
            "unit": unit
        })

    return parsed_items


if __name__ == "__main__":
    # Test case from spec
    raw_input = "3 eggs, 200g flour, 1 liter milk"
    result = parse_pantry(raw_input)
    print(result)
    
    # Expected:
    # [
    #   {'name': 'eggs', 'quantity': 3, 'unit': 'count'},
    #   {'name': 'flour', 'quantity': 200, 'unit': 'g'},
    #   {'name': 'milk', 'quantity': 1, 'unit': 'liter'}
    # ]
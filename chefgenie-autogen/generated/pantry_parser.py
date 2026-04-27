import re
from typing import List, Dict, Any


def parse_pantry(raw_text: str) -> List[Dict[str, Any]]:
    """
    Parses raw text input into a structured list of pantry items.

    Args:
        raw_text (str): Raw text of pantry items (e.g., "3 eggs, 200g flour, milk").

    Returns:
        List[Dict[str, Any]]: A list of dictionaries where each dictionary represents
            a pantry item with 'name', 'quantity', and 'unit'.
    """
    items = []
    # Split by comma to get individual item strings
    raw_items = [item.strip() for item in raw_text.split(',')]

    for item in raw_items:
        if not item:
            continue
        
        # Pattern to match optional quantity, optional unit, and name
        # Units can be abbreviations (g, kg, ml, l) or full words (liter, gram, etc.)
        # Quantity is a number. If no number, default to 1.
        # Unit might be attached to the number (e.g., "200g") or separate (e.g., "1 liter").
        
        # Regex explanation:
        # ^(\d+\.?\d*)? - Optional leading number (quantity)
        # ([a-zA-Z]+)?  - Optional unit immediately following number (if attached)
        # \s*           - Optional whitespace
        # (.+)          - Remaining text as name
        
        match = re.match(r'^(\d+\.?\d*)?\s*([a-zA-Z]+)?\s*(.+)$', item)
        
        if match:
            quantity_str, unit_str, name = match.groups()
            
            # Handle quantity
            if quantity_str:
                quantity = float(quantity_str)
                if quantity.is_integer():
                    quantity = int(quantity)
            else:
                quantity = 1
            
            # Handle unit
            if unit_str:
                unit = unit_str.lower()
            else:
                unit = "count"
            
            # Normalize some common units
            if unit == 'l':
                unit = 'liter'
            elif unit == 'g':
                unit = 'g'
            elif unit == 'kg':
                unit = 'kg'
            elif unit == 'ml':
                unit = 'ml'
            
            # Clean up name (remove any trailing/leading whitespace)
            name = name.strip()
            
            items.append({
                "name": name,
                "quantity": quantity,
                "unit": unit
            })
        else:
            # Fallback for simple names without numbers or units
            items.append({
                "name": item.strip(),
                "quantity": 1,
                "unit": "count"
            })
            
    return items


if __name__ == "__main__":
    # Test case from specification
    test_input = "3 eggs, 200g flour, 1 liter milk"
    expected_output = [
        {"name": "eggs", "quantity": 3, "unit": "count"},
        {"name": "flour", "quantity": 200, "unit": "g"},
        {"name": "milk", "quantity": 1, "unit": "liter"}
    ]
    
    result = parse_pantry(test_input)
    
    print(f"Input: {test_input}")
    print(f"Output: {result}")
    print(f"Expected: {expected_output}")
    
    # Verify match
    if result == expected_output:
        print("Test Passed!")
    else:
        print("Test Failed!")
import re
from typing import Optional


def convert_xml_string_to_float_or_null(xml_str: str) -> Optional[float]:
    converted_float = float(xml_str)
    if converted_float == -99999:
        return None
    else:
        return converted_float


def extract_float(input_string: str) -> Optional[float]:
    # Define a regular expression pattern to match float values
    pattern = r"[-+]?\d*\.\d+|\d+"
    # Replace , by .
    input_string = input_string.replace(",", ".")
    # Find all occurrences of the pattern in the input string
    matches = re.findall(pattern, input_string)

    if matches:
        # Convert the matched string to a float
        float_value = float(matches[0])
        return float_value
    else:
        return None  # Return None if no float value is found


# Utility function to convert to float if text exists, otherwise return None
def float_if_exist(text: str) -> Optional[float]:
    return extract_float(text) if text is not None else None


# def are_floats_none_or_near(value1: float, value2: float, tolerance=1e-2) -> bool:
#     if value1 is None and value2 is None:
#         return True
#     elif value1 is None or value2 is None:
#         return False
#     else:
#         return abs(value1 - value2) <= tolerance

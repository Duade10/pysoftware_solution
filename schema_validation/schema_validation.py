import pprint
from typing import Dict, Union, Any

import jsonschema
from jsonschema import validate

# Constants
SERIAL_NUMBER_RANGE = [
    "C25CTW00000000001470",
    "C25CTW00000000001471",
    "C25CTW00000000001472",
    "C25CTW00000000001473",
    "C25CTW00000000001474",
    "C25CTW00000000001475",
    "C25CTW00000000001476",
    "C25CTW00000000001477",
    "C25CTW00000000001478"
]

# JSON schema or JSON Object
schema = {
    "type": "object",
    "properties": {
        "comment": {
            "type": "string",
            "minLength": 1
        },
        "Internet_hubs": {
            "type": "array",
            "uniqueItems": True,
            "minItems": 1,
            "items": {
                "required": [
                    "id",
                    "serial_number"
                ],
                "properties": {
                    "id": {
                        "type": "string",
                        "minLength": 1
                    },
                    "serial_number": {
                        "type": "string",
                        "minLength": 1
                    }
                }
            }
        }
    },
    "required": [
        "comment",
        "Internet_hubs"
    ]
}


def validate_hubs(hub: Dict) -> bool:
    """
    This function check if a hub has similar characteristics with the rest of the hubs.

    The criteria being used to check: is if the id contains "mn" and the last charater is a digit.
    
    Args:
        hub (Dict) -- A dict containing all the hub extracted from the original data "internt hubs"

    Returns: 
        It resturns a boolean True or False if he hubs meets the required criteria
    """

    return hub["id"].startswith("mn") and hub["id"][2].isdigit()


def validate_serial_numbers(data: Dict) -> Union[Dict, str]:
    """
    Validates the input data against a predefined JSON schema.

    Args:
        data (Dict): The JSON object (or Python dictionary) to be validated.

    Returns:
        Union[Dict, str]: The original data if it is valid according to the schema,
                          or an error message string if validation fails.

    Raises:
        jsonschema.exceptions.ValidationError: If the data does not conform to the schema.
    """
    try:

        validate(instance=data, schema=schema)
        return data

    except jsonschema.exceptions.ValidationError as e:
        return f"Invalid JSON schema: {e.message}"


def assign_serial_numbers(validated_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    It assigns serial numbers to each hub based on the reverse order, matching the id to the serial numbers

    Args:
        validated_data (Dict[str, Any]): JSON object that was been validated.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary containing the original data 
                                   and an updated version.
    """
    original_data = validated_data  # Keeps originital data so I can display at the end.

    reversed_serial_numbers = SERIAL_NUMBER_RANGE[::-1]  # Reverse serial number range
    updated_hubs = []
    current_hubs = validated_data["Internet_hubs"]

    for hub in current_hubs:
        if validate_hubs(hub):
            hub_copy = hub.copy()  # Make a copy to avoid modifying the original data
            index = int(hub_copy["id"][2]) - 1

            if 0 <= index < len(reversed_serial_numbers):
                hub_copy["serial_number"] = reversed_serial_numbers[
                    index]  # Assign serial number to the right up using the 0 index digit format
            updated_hubs.append(hub_copy)

    # updated data structure with the modified hubs
    updated_data = {
        "comment": validated_data.get("comment", ""),
        "Internet_hubs": updated_hubs
    }

    return {"original": original_data, "updated": updated_data}


def validate_and_assign_serial_numbers(data: Dict) -> Union[Dict, str]:
    """
    It contains two functions that firstly validate the input data and then
    assign serial numbers to the hubs based on specific criteria

    
    Args:
        data (Dict): A JSON object (or Python dictionary) containing the 
                     internet hubs information.

    Returns:
        Union[Dict, str]: A dictionary with validated and updated serial
                          numbers if successful, or an error message.

    Raises:
        Exception: If validation or assignment of the (ID or serial numbers) fails.
    """
    try:

        validated_data = validate_serial_numbers(data)
        result = assign_serial_numbers(validated_data)
        return result

    except Exception as e:
        return f"Couldn't assign and validate serial numbers: {e}"


data: Dict = {
    "comment": "Do NOT commit local changes to this file to source control",
    "Internet_hubs": [
        {"id": "men1", "serial_number": "C25CTW00000000001470"},
        {"id": "mn1", "serial_number": "<serial number here>"},
        {"id": "mn2", "serial_number": "<serial number here>"},
        {"id": "mn3", "serial_number": "<serial number here>"},
        {"id": "mn4", "serial_number": "<serial number here>"},
        {"id": "mn5", "serial_number": "<serial number here>"},
        {"id": "mn6", "serial_number": "<serial number here>"},
        {"id": "mn7", "serial_number": "<serial number here>"},
        {"id": "mn8", "serial_number": "<serial number here>"},
        {"id": "mn9", "serial_number": "<serial number here>"}
    ]
}

if __name__ == "__main__":
    pprint.pprint(validate_and_assign_serial_numbers(data))
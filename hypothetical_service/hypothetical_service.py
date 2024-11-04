import os
from typing import List, Dict, Any

import pandas as pd
import requests

# Constants
API_KEY = 'ssfdsjfksjdhfgjfgvjdshgvshgkjsdlgvkjsdgjkl'
BASE_URL = 'https://pysoftware.com/v1'
HEADERS = {'X-API-KEY': API_KEY}


def get_customer_numbers():
    """
    Retrieve the total customer numbers.

    This function retrieves the total number of customer numbers from the
    API server. The result is returned as an integer.

    Returns:
        int: The total number of customer numbers.
    """
    response = requests.get(f"{BASE_URL}/customer_numbers", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def get_address(customer_number: int) -> Dict:
    """
    Retrieve address for a specific customer number.

    This function retrieves the address information for a single customer
    number from the API server. The result is returned as a JSON object.

    Args:
        customer_number (int): The customer number for which the address
            information is to be retrieved.

    Returns:
        Dict: The address information for the customer number.
    """
    response = requests.get(f"{BASE_URL}/address_inventory/{customer_number}", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def validate_address(address: Dict) -> bool:
    """d
    Validate the address fields.

    Check that a given address dictionary contains all the required fields
    and that they are not empty.

    Args:
        address (Dict): The address dictionary that will be validate

    Returns:
        bool: True if the address is valid, otherwise it is False.
    """
    required_fields: List[str] = ['id', 'first_name', 'last_name', 'street', 'postcode', 'state', 'country', 'lat',
                                  'lon']
    for field in required_fields:
        if field not in address or address[field] is None:
            return False
    return True


def retrieve_addresses() -> List[Dict[str, Any]]:
    """Retrieve and validate all customer addresses.

    Retrieve all customer addresses from the API server and validate them.
    If the address is invalid, a message is printed to the console and the
    address is not included in the returned list.

    Returns:
        List[Dict[str, Any]]: A list of valid customer addresses.
    """
    customer_numbers: int = get_customer_numbers()
    all_addresses: List = []

    for customer_number in range(1, customer_numbers + 1):
        try:
            address = get_address(customer_number)
            if validate_address(address):
                all_addresses.append(address)
            else:
                print(f"Invalid address data for customer number: {customer_number}")
        except Exception as e:
            print(f"Error retrieving address for customer number {customer_number}: {e}")

    return all_addresses


def save_addresses_to_csv(addresses: List[Dict[str, Any]], filename: str) -> str:
    """
    Save addresses intto a CSV file.

    Args:
        addresses (List[Dict[str, Any]]): A list of dictionaries containing address information.
        filename (str): The filename of the file to save the CSV file as.

    Returns:
        str: The path to the saved CSV file.
    """
    df = pd.DataFrame(addresses)
    df.to_csv(filename, index=False)
    return os.path.abspath(filename)


def main():
    # Retrieve addresses
    addresses = retrieve_addresses()

    # Save to CSV
    csv_filename = "customer_addresses.csv"
    csv_path = save_addresses_to_csv(addresses, csv_filename)

    # Communicate the path of the saved CSV file
    print(f"The addresses have been saved to: {os.path.abspath(csv_path)}")

    # Return the addresses in a tabular form
    print("\nCustomer Addresses:")
    print(pd.DataFrame(addresses))


if __name__ == "__main__":
    main()

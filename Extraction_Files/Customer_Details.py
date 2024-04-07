import json
from zipfile import ZipFile
import re

class Customer:
    def __init__(self):
        pass

    def customer_details(zip_file_path):
        """
        Extracts customer details from a structured JSON file inside a ZIP archive.

        Args:
            zip_file_path (str): Path to the ZIP archive containing the structured JSON file.

        Returns:
            tuple: A tuple containing address line 1, address line 2, email, name, and phone number.
        """

        address_line1 = None
        address_line2 = None
        email = None
        name = None
        phone_number = None

        json_file = 'structuredData.json'

        # Extract the structured JSON file from the ZIP archive
        with ZipFile(zip_file_path, 'r') as zf:
            zf.extract(json_file)

        # Load the structured JSON data
        with open(json_file, 'r') as file:
            data = json.load(file)
            customer_details = None
            vertical_business_desc = None

            # Iterate through the elements in the JSON data
            for item in data['elements']:

                # Check if vertical business description is set and the item has bounds
                if vertical_business_desc and item.get('Bounds'):

                    # Check if the item's bounds match the vertical business description and has text
                    if item.get('Bounds')[0] == vertical_business_desc and item.get('Text'):
                        customer_details += item.get('Text')

                # Check if the item has text and contains 'BILL'
                if item.get('Text') and 'BILL' in item.get('Text'):

                    # Check if the item has bounds
                    if item.get('Bounds'):

                        # Set the vertical business description and reset customer details
                        vertical_business_desc = item.get('Bounds')[0]
                        customer_details = ""

        # Extract phone number using regex pattern
        pattern = r'\d{3}-\d{3}-\d{4}'
        phone_numbers = re.findall(pattern, customer_details)
        if phone_numbers:
            phone_number = phone_numbers[0].strip()

        # Extract email using regex pattern
        pattern = r'\S+@\S+'
        emails = re.findall(pattern, customer_details)
        if emails:
            email = emails[0].strip()

        # Extract name based on email presence
        if email:
            name_tokens = customer_details.split()
            if email in name_tokens:
                name = " ".join(name_tokens[:name_tokens.index(email)])

        # Append additional word to email if it does not end with '.com'
        if email and not email.endswith('com'):
            email += customer_details.split()[customer_details.split().index(email) + 1]

        # Extract address lines based on phone number presence
        if phone_number:
            address_tokens = customer_details.split()
            if phone_number in address_tokens:
                phone_index = address_tokens.index(phone_number)
                address_line1 = " ".join(address_tokens[phone_index + 1: phone_index + 4])
                address_line2 = " ".join(address_tokens[phone_index + 4:])

        # Print a message to indicate the function return
        print("Return from customer_Details")

        # Return the extracted customer details as a tuple
        return address_line1, address_line2, email, name, phone_number






        

            




    
    
    

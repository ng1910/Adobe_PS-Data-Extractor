from zipfile import ZipFile
import re
import json

class Business_details:

    def __init__(self):
        pass

    def get_details(zip_file_path):
        """
        Extracts business details from a structured JSON file within a given zip file.

        Args:
            zip_file_path (str): Path to the zip file containing the structured JSON file.

        Returns:
            Tuple: A tuple containing the extracted business details in the following order:
                - city (str): City of the business.
                - country (str): Country of the business.
                - description (str): Description of the business.
                - name (str): Name of the business.
                - street (str): Street address of the business.
                - zipcode (str): Zip code of the business.
                - invoice_no (str): Invoice number associated with the business.
                - issue_date (str): Issue date of the invoice.

        Raises:
            FileNotFoundError: If the specified JSON file within the zip file is not found.
        """

        json_file = 'structuredData.json'

        with ZipFile(zip_file_path, 'r') as zf:
            zf.extract(json_file)

        # Load the JSON data from the file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Initialize variables to store extracted information
        city = None
        country = None
        description = None
        name = None
        street = None
        zipcode = None
        vertical = None
        horizontal = None
        details = ""

        # Extract business details from the JSON data
        k = False
        for items in data['elements']:

            if items.get('Text') and k is True :
                k = False
                description = items.get('Text')


            if items.get('TextSize') and int(items.get('TextSize')) > 20 : 
                name = items.get('Text')
                vertical = items.get('Bounds')[2]
                horizontal = items.get('Bounds')[3]
                k = True

        # Extract additional details based on text position
        for items in data['elements']:
            if items.get('Text') and items.get('Bounds')[3] > horizontal and items.get('Bounds')[2] < vertical :
                    details += items.get('Text')

        # Process the extracted details to obtain specific information
        if details:
            token = details.split()
        
        street = " ".join(token[2:5])
        street = street.replace(',','')
        
        city = token[5]
        city = city.replace(',','')

        country = " ".join(token[6:8])

        zipcode = token[8]

        # Extract invoice details
        invoice_details = ""
        invoice_no = None
        issue_date = None

        for items in data['elements']:
            if items.get('Text') and items.get('Bounds')[3] > horizontal and items.get('Bounds')[2] > vertical :
                invoice_details += items.get('Text')

        #Invoice# NL57EPAS7793742478 Issue date 12-05-2023

        invoice_token = invoice_details.split()

        invoice_no = invoice_token[1]

        issue_date = invoice_token[4]

        # Print a message to indicate the function return
        print("Return from Business_Details")

        # Return the extracted business details as a tuple
        return city, country, description, name, street, zipcode, invoice_no, issue_date
        
        
        






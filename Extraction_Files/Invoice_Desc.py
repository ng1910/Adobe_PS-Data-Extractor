import json
import re
from zipfile import ZipFile

class invoice_details :

    def __init__(self):
        """
        Initializes an invoice_details object.
        """
        pass

    def invoice(zip_file_path):
        """
        Extracts invoice details from the specified zip file.

        Args:
            zip_file_path (str): The path of the zip file.

        Returns:
            Tuple[str, str, str]: A tuple containing the invoice description, due date, and tax.

        Raises:
            None
        """
        
        json_file = 'structuredData.json'

        # Extract the structuredData.json file from the zip file
        with ZipFile(zip_file_path, 'r') as zf:
            zf.extract(json_file)

        # Load the contents of the structuredData.json file
        with open(json_file, 'r') as file:
            data = json.load(file)

        invoice_desc = ""
        date = ""
        due_date = None
        vertical_1 = None
        vertical_2 = None
        Horizontal_1 = None
        Horizontal_2 = None
        K = False
        
        # Iterate through the elements in the JSON data
        for items in data['elements']:
            if items.get('Text') and 'DETAILS' in items.get('Text'):
                vertical_1 = items.get('Bounds')[0]
                Horizontal_1 = items.get('Bounds')[3]

            if items.get('Text') and K:
                K = False
                date = items.get('Text')

            if items.get('Text') and 'PAYMENT' in items.get('Text'):
                vertical_2 = items.get('Bounds')[0]

            if items.get('Text') and 'QTY' in items.get('Text'):
                Horizontal_2 = items.get('Bounds')[3]

        # Extract the invoice description and date
        for items in  data['elements']:
            if items.get('Text'):
                vert_temp = items.get('Bounds')[2]
                hori_temp = items.get('Bounds')[3]
                if items.get('Text') and vert_temp > vertical_1 and vert_temp < vertical_2 and hori_temp < Horizontal_1 and hori_temp > Horizontal_2:
                    invoice_desc += items.get('Text')
                if items.get('Text') and vert_temp > vertical_2 and hori_temp < Horizontal_1 and hori_temp > Horizontal_2:
                    date += items.get('Text')
            
        # Extract the due date from the date string
        date_token = date.split()
        due_date = date_token[2]

        # Extract the tax information
        tax = None
        M = False
        for items in data['elements']:
            if items.get('Text') and M:
                if '$' in items.get('Text') or "Total" in items.get('Text'):
                    continue
                
                M = False
                tax = items.get('Text')

            if items.get('Text') and "Tax % " in items.get('Text'):
                M = True
                if items.get('Text').split()[-1] != '%':
                    M = False
                    tax = items.get('Text')[-1]
    
        
        print("Return from invoice_Desc")
        # Return the extracted invoice details
        return invoice_desc, due_date, tax






        

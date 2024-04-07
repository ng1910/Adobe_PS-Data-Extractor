import pandas as pd
import re
import os.path
import logging
from tqdm import tqdm


from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation


from Extraction_Files.extract_txt_table_info_from_pdf import Table_Extractor
from Extraction_Files.Extract_Table_Data import InvoiceTable
from Extraction_Files.Invoice_Desc import invoice_details
from Extraction_Files.Customer_Details import Customer
from Extraction_Files.Business_Details import Business_details

# Configure logging
logging.basicConfig(level=os.environ.get("LOGLEVEL"))

class Final_Extraction:
    def __init__(self, base_path, input_path, output_path):
        """
        Initializes the Final_Extraction class.

        Args:
            base_path (str): The base path for the extraction process.
            input_path (str): The path to the input PDF files.
            output_path (str): The path to save the extracted data.

        """
        self.base_path = base_path
        self.input_path = input_path
        self.output_path = output_path
        self.table_extractor = Table_Extractor(base_path=self.base_path)

    def extraction(self):
        """
        Perform the extraction process on the PDF files.

        """
        input_files = [file for file in os.listdir(self.input_path) if file.endswith('.pdf')]
        input_files = sorted(input_files, key=lambda x: (int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else x[:-4], x))

        data = pd.DataFrame()

        for current_file in tqdm(input_files, desc="pdf invoice processing", unit="file"):
            current_file = current_file.split('.')[0]

            try:
                zip_file_path = self.table_extractor.Get_Table(current_file)
                data_frame = pd.DataFrame()
                data_frame = InvoiceTable.get_output(zip_file_path)

                 # Extract business details from the zip file and assign them to respective columns in the DataFrame
                data_frame[['Bussiness__City', 'Bussiness__Country', 'Bussiness__Description', 'Bussiness__Name', 'Bussiness__StreetAddress', 'Bussiness__Zipcode', 'Invoice__Number', 'Invoice__IssueDate']] = Business_details.get_details(zip_file_path)

                # Extract customer details from the zip file and assign them to respective columns in the DataFrame
                data_frame[['Customer__Address__line1', 'Customer__Address__line2', 'Customer__Email', 'Customer__Name', 'Customer__PhoneNumber']] = Customer.customer_details(zip_file_path)

                 # Extract invoice details from the zip file and assign them to respective columns in the DataFrame
                data_frame[['Invoice__Description', 'Invoice__DueDate', 'Invoice__Tax']] = invoice_details.invoice(zip_file_path)

                # Select only the required columns in the desired order
                data_frame = data_frame[['Bussiness__City', 'Bussiness__Country', 'Bussiness__Description', 'Bussiness__Name',
                             'Bussiness__StreetAddress', 'Bussiness__Zipcode', 'Customer__Address__line1',
                             'Customer__Address__line2', 'Customer__Email', 'Customer__Name', 'Customer__PhoneNumber',
                             'Invoice__BillDetails__Name','Invoice__BillDetails__Quantity','Invoice__BillDetails__Rate',
                             'Invoice__Description', 'Invoice__DueDate', 'Invoice__IssueDate', 'Invoice__Number',
                             'Invoice__Tax']]
                
                # Add a column to store the file name
                data_frame['File Name'] = current_file
                
                 # Concatenate the current data frame with the overall data frame
                data = pd.concat([data, data_frame], ignore_index=True)

                # Remove the processed zip file
                os.remove(zip_file_path)

            except Exception as e:
                # Print error message and log the exception
                print("ERROR IN ---->", current_file, "<<<<<<<<<<")
                logging.error(str(e))
    
        # Write the final data frame to the output CSV file
        data.to_csv(self.output_path, index=False)


# usage of the Final_Extraction class
base_path = os.getcwd()
input_path = os.path.join(base_path, 'Input_Files')
output_path = os.path.join(base_path, 'output_file.csv')


# Create an instance of the Final_Extraction class
processor = Final_Extraction(base_path, input_path, output_path)

# Call the extraction method to start the data extraction process
processor.extraction()

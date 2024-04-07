from zipfile import ZipFile
import pandas as pd

class InvoiceTable:
    def __init__(self):
        pass

    def get_output(zip_file_path):
        """
        Extracts and processes invoice data from a ZIP archive containing an Excel file.

        Args:
            zip_file_path (str): Path to the ZIP archive containing the invoice Excel file.

        Returns:
            pandas.DataFrame: Processed invoice data as a DataFrame.

        Raises:
            ValueError: If the header or data table is missing in the ZIP archive.
        """

        # Initialize variables
        data_file = None
        header_file = None
        col_num = None

        with ZipFile(zip_file_path, 'r') as zfile:
            files_name = sorted(zfile.namelist())

            # Extract and read Excel files from the ZIP archive
            for file_name in files_name:
                if file_name.endswith('.xlsx'):
                    zfile.extract(file_name)
                    data_frame = pd.read_excel(file_name)
                    col_num = data_frame.shape[1]

                # Check if the number of columns is as expected
                if col_num == 4:
                    if header_file is None:
                        header_file = file_name
                    else:
                        data_file = file_name
                        break

            # Raise an error if the header or data table is missing
            if header_file is None or data_file is None:
                raise ValueError("Failed to load either the header or data table.")

            # Extract and process header and data files
            headers = zfile.extract(header_file)
            data_files = zfile.extract(data_file)

            # Read header columns and replace special characters
            columns = pd.read_excel(headers, header=None).replace(to_replace=r'_x000D_', value='', regex=True)
            data_frame = pd.read_excel(data_files, header=None)
            columns = list(columns.iloc[0,:])

            # Set column names and drop the last column
            data_frame.columns = columns
            data_frame = data_frame.replace(to_replace=r'_x000D_', value='', regex=True)
            data_frame = data_frame.drop(data_frame.columns[-1], axis=1)

            # Rename columns to match the expected names
            new_column_names = {'ITEM ':'Invoice__BillDetails__Name','QTY ':'Invoice__BillDetails__Quantity','RATE ':'Invoice__BillDetails__Rate'}
            data_frame = data_frame.rename(columns=new_column_names)

            # Replace any remaining special characters
            data_frame = data_frame.reset_index(drop=True)
            
            # Return the processed invoice data
            print("Return from Extract_Table")
            return data_frame
        

        


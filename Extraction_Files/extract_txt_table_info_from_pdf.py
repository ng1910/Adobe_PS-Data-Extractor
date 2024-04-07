# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging
import time
import os.path

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class Table_Extractor:

    def __init__(self, base_path):
        """
        Initializes a Table_Extractor object.

        Args:
            base_path (str): The base path for file operations.
        """
        self.base_path = base_path

    def Get_Table(self, input_file_path):
        """
        Extracts tables from the specified input file.

        Args:
            input_file_path (str): The path of the input file.

        Returns:
            str: The path of the saved result file containing extracted tables.

        Raises:
            Exception: If the maximum number of retries is exceeded.
        """

        MAX_RETRIES = 3
        RETRY_DELAY = 5

        retries = 0
        while retries < MAX_RETRIES:
            try:
                # get base path.

                # Initial setup, create credentials instance.
                credentials = Credentials.service_account_credentials_builder() \
                    .from_file(self.base_path + "/pdfservices-api-credentials.json") \
                    .build()

                # Create an ExecutionContext using credentials and create a new operation instance.
                execution_context = ExecutionContext.create(credentials)
                extract_pdf_operation = ExtractPDFOperation.create_new()

                # Set operation input from a source file.
                source = FileRef.create_from_local_file(self.base_path + '/Input_Files/' + input_file_path +".pdf")
                extract_pdf_operation.set_input(source)

                # Build ExtractPDF options and set them into the operation
                extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
                    .with_element_to_extract(ExtractElementType.TEXT) \
                    .with_element_to_extract(ExtractElementType.TABLES) \
                    .build()
                extract_pdf_operation.set_options(extract_pdf_options)

                # Execute the operation.
                result: FileRef = extract_pdf_operation.execute(execution_context)

                # Save the result to the specified location.
                result_path = self.base_path + "/output/ExtractTextTableInfoFromPDF.zip"
                result.save_as(result_path)

                # Print a message to indicate the function return
                print("Return from adobe")
                return result_path
            except (ServiceApiException, ServiceUsageException, SdkException):
                # Log the exception and handle the error case
                logging.exception("Exception encountered while executing operation" + input_file_path)
                print("API call timed out. Retrying...")
                retries += 1
                time.sleep(RETRY_DELAY)

        # If the maximum number of retries is exceeded, raise an exception
        raise Exception("Max retries exceeded. Unable to complete API call.")

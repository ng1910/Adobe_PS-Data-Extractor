# Adobe_PS
This project aims to extract specific data from PDF files using the Adobe Extract API and store it in a CSV file.

## Getting Started
Follow the instructions below to set up and use Adobe.PS.

### Prerequisites

- Anaconda: Make sure you have Anaconda installed on your system. You can download it from the official Anaconda website: https://www.anaconda.com/products/individual
- API Credentials: Obtain API credentials from the Adobe Developer website by following these steps:
  Visit https://developer.adobe.com/document-services/apis/pdf-extract/
  Generate the necessary API credentials by following the provided instructions.

### Installation

1. Clone the repository to your local machine or download the project files as a ZIP archive.
   
2. Open Anaconda Navigator or launch the Anaconda Prompt.
   
3. Create a new conda environment for the project. You can use the Anaconda Navigator GUI or the following command in the Anaconda 
   Prompt: 
```shell
conda create --name adobe-ps python=3.10
```

4. Activate the newly created conda environment. In the Anaconda Prompt, run:
```shell
conda activate adobe-ps
```
5. Navigate to the project directory using the cd command in the Anaconda Prompt.
   
6. Install the required dependencies using pip and the provided requirements.txt file:
```shell
pip install -r requirements.txt
```
7. Place your API credentials file in the project directory. Make sure it is named credentials.json.
   
8. You are now ready to run the project and extract data from PDF files using the Adobe Extract API.

## Usage
To use the project, follow these steps:

1. Make sure you have activated the conda environment in the Anaconda Prompt.

2. Place your PDF files in the designated input folder.

3. Run the main script to initiate the data extraction process:
```shell
python main.py
```
4. The extracted data will be saved in a CSV file named output.csv in the project directory.

## Contact Information

For any questions, suggestions, or feedback, please contact the project maintainer at amanraghu1c1301@gmail.com.

## Acknowledgments

I would like to express my sincere gratitude to the organizers of the PapyrusNebulae 2023 Document Cloud Hackathon for providing me with this exceptional learning opportunity.




 

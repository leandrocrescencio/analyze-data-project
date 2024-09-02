# Analyze Data Project
This project contains a Python script that processes and analyzes data in JSON format. The script is Dockerized for ease of deployment and execution.

## Project Structure

```python
analyze-data-project/
│
└── data/                          # Data folder
     │
     ├── rt-feed-debug.json        # Sample JSON data file 1 (input)
     ├── rt-feed-record.json       # Sample JSON data file 2 (input)
├── Dockerfile                     # Docker configuration file
├── analyze_data.py                # Python script for data analysis
├── README.md                      # Project documentation (this file)
└── test_analyze_data.py           # Unittest to validate the analyze_data.py
```

## Requirements
Docker: Make sure Docker is installed on your system. You can download and install Docker from the official website.

## Setup and Execution
**1. Clone the Repository**
Clone this repository to your local machine:

``` cd analyze-data-project ``` 

**2. Build the Docker Image**
<br>In the project directory, build the Docker image using the following command:

``` docker build -t analyze-data . ```

<br>This command will create a Docker image named analyze-data based on the instructions in the Dockerfile.

**3. Run the Docker Container**
<br>After building the image, run the Docker container using:

``` docker run --rm -v "$(pwd)":/app analyze-data ```

This command will:
* Run the Python script (`analyze_data.py`) inside the Docker container.
* Mount the current directory into the container’s /app directory to access the JSON data file.

**4. Output**

The script will:
* Count the total number of distinct stories in the provided data inside the the `data` folder.
* Detect and report any missing analytics based on the DOCUMENT_RECORD_INDEX and DOCUMENT_RECORD_COUNT fields, and print it
* Validate the format of the RP_ENTITY_ID field against the expected pattern and print the result.


**5. Running the tests**

``` python -m unittest test_analyze_data.py ```

This command will ran the five test to validate the methods in the `analyze_data.py`


## Python Script Analysis 

### Functions
- **load_data(filepath):** Loads JSON data from the data folder.
- **count_distinct_stories(data):** Counts the total number of distinct stories based on RP_DOCUMENT_ID.
- **find_missing_analytics(data):** Identifies and reports any missing analytics records for a story.
- **validate_entity_id(data):** Validates the RP_ENTITY_ID field to ensure it matches the expected format.
- **analyze_file(data):** Receives the data to apply the above methods 

### Usage 

The code is ready to handle different data files, replace the rt-feed-record.json or just add the data file in the data folder and the `analyze_data.py` script will capture it.<br>
The script is designed to handle data in the JSON Lines format, where each line is a JSON object.<br>
It checks for missing analytics and validates the format of certain fields, printing the results to the console.<br>

## Conclusion
This project demonstrates how to process and validate real-time analytics data efficiently within a Dockerized environment. Feel free to modify the script or Dockerfile to suit your needs.

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

`cd analyze-data-project` 

**2. Build the Docker Image**
<br>In the project directory, build the Docker image using the following command:

`docker build -t analyze-data .`

<br>This command will create a Docker image named analyze-data based on the instructions in the Dockerfile.

**3. Run the Docker Container**
<br>After building the image, run the Docker container using:

`docker run --rm -v "$(pwd)":/app analyze-data`

This command will:
* Run the Python script (analyze_data.py) inside the Docker container.
* Mount the current directory into the container’s /app directory to access the JSON data file.

**4. Output**

The script will:
* Count the total number of distinct stories in the provided data file.
* Detect and report any missing analytics based on the DOCUMENT_RECORD_INDEX and DOCUMENT_RECORD_COUNT fields.
* Validate the format of the RP_ENTITY_ID field against the expected pattern.
* The results will be printed in the terminal.

The code is ready to handle different data files, replace the rt-feed-record.json or just add the data file in the data folder and the analyze_data.py script will capture it

**5. Running the test**

`python -m unittest test_analyze_data.py`

This command will ran the 5 test for validate the methods in the analyze_data.py

## Conclusion
This project demonstrates how to process and validate real-time analytics data efficiently within a Dockerized environment. Feel free to modify the script or Dockerfile to suit your needs.

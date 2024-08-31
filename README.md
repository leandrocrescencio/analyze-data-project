Analyze Data Project
This project contains a Python script that processes and analyzes data in JSON format. The script is Dockerized for ease of deployment and execution.

Project Structure

analyze-data-project/
│
├── Dockerfile                   # Docker configuration file
├── analyze_data.py              # Python script for data analysis
├── rt-feed-record.json          # Sample JSON data file (input)
└── README.md                    # Project documentation (this file)

Requirements
Docker: Make sure Docker is installed on your system. You can download and install Docker from the official website.

Setup and Execution
1. Clone the Repository
Clone this repository to your local machine:

cd analyze-data-project
2. Build the Docker Image
In the project directory, build the Docker image using the following command:

docker build -t analyze-data .
This command will create a Docker image named analyze-data based on the instructions in the Dockerfile.

3. Run the Docker Container
After building the image, run the Docker container using:

docker run --rm -v "$(pwd)":/app analyze-data
This command will:

Run the Python script (analyze_data.py) inside the Docker container.
Mount the current directory into the container’s /app directory to access the JSON data file.

4. Output
The script will:

Count the total number of distinct stories in the provided data file.
Detect and report any missing analytics based on the DOCUMENT_RECORD_INDEX and DOCUMENT_RECORD_COUNT fields.
Validate the format of the RP_ENTITY_ID field against the expected pattern.
The results will be printed in the terminal.

Explanation of the Python Script
Functions
load_data(filepath): Loads JSON data from the provided file.
count_distinct_stories(data): Counts the total number of distinct stories based on RP_DOCUMENT_ID.
find_missing_analytics(data): Identifies and reports any missing analytics records for a story.
validate_entity_id(data): Validates the RP_ENTITY_ID field to ensure it matches the expected format.
Usage
The script is designed to handle data in the JSON Lines format, where each line is a JSON object.
It checks for missing analytics and validates the format of certain fields, printing the results to the console.
Customization
To use a different data file, replace the rt-sample-record.json file with your own data file and ensure that the file_path variable in the analyze_data.py script points to /data/rt-feed-record.json.

Conclusion
This project demonstrates how to process and validate real-time analytics data efficiently within a Dockerized environment. Feel free to modify the script or Dockerfile to suit your needs.

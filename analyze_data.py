import json
import re
import time
import os
import glob
from collections import defaultdict

def load_data(filepath):
    try:
        print(f"\nLoading data from {filepath}...")
        with open(filepath, 'r') as file:
            data = [json.loads(line) for line in file]
        print("\nData loaded successfully!")
        return data
    except FileNotFoundError:
        print(f"\nError: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"\nError: Failed to decode JSON in file '{filepath}'. {e}")
        return []

def count_distinct_stories(data):
    distinct_stories = set(record['RP_DOCUMENT_ID'] for record in data)
    return len(distinct_stories)

def find_missing_analytics(data):
    story_records = defaultdict(list)
    expected_counts = {}

    for record in data:
        doc_id = record['RP_DOCUMENT_ID']
        story_records[doc_id].append(record['DOCUMENT_RECORD_INDEX'])
        if doc_id not in expected_counts:
            expected_counts[doc_id] = record['DOCUMENT_RECORD_COUNT']

    missing_analytics = {}
    
    for doc_id, indices in story_records.items():
        expected_count = expected_counts[doc_id]
        actual_count = len(indices)

        if actual_count != expected_count:
            missing_indices = set(range(1, expected_count + 1)) - set(indices)
            if missing_indices:
                missing_analytics[doc_id] = sorted(missing_indices)

    return missing_analytics

def validate_entity_id(data):
    valid_id_pattern = re.compile(r'^[A-Z0-9]{6}$')
    invalid_ids = [record['RP_ENTITY_ID'] for record in data if not valid_id_pattern.match(record['RP_ENTITY_ID'])]
    return invalid_ids

def analyze_file(file_path):
    # Load data from file
    data = load_data(file_path)
    if not data:
        return  # Exit if data loading fails
    
    # Count distinct stories
    distinct_stories = count_distinct_stories(data)
    print(f'\nTotal number of distinct stories: {distinct_stories}\n')

    # Find missing analytics
    missing_analytics = find_missing_analytics(data)
    if missing_analytics:
        print('Stories with missing analytics:')
        for doc_id, missing_indices in missing_analytics.items():
            print(f'{doc_id}: Missing indices {sorted(missing_indices)}\n')
    else:
        print('No missing analytics found.\n')

    # Validate RP_ENTITY_ID
    invalid_entity_ids = validate_entity_id(data)
    if invalid_entity_ids:
        print(f'Invalid RP_ENTITY_IDs: {invalid_entity_ids}\n')
    else:
        print('All RP_ENTITY_IDs are valid.\n')

def main():
    # Directory containing the JSON files
    data_directory = 'data/'

    # List all JSON files in the directory
    json_files = glob.glob(os.path.join(data_directory, '*.json'))
    
    if not json_files:
        print(f"No JSON files found in '{data_directory}'.")
        return
    
    for file_path in json_files:
        analyze_file(file_path)

if __name__ == "__main__":
    main()

import unittest
from unittest.mock import patch, mock_open
from analyze_data import load_data, count_distinct_stories, find_missing_analytics, validate_entity_id

class TestAnalyzeData(unittest.TestCase):
    
    def setUp(self):
        # Sample data with no missing indices
        self.sample_data = [
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 3, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC002", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "XYZ789"},
            {"RP_DOCUMENT_ID": "DOC002", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "XYZ789"}
        ]
        # Sample data with missing indices (DOC001 missing index 3, DOC003 missing index 1)
        self.sample_data_2 = [
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC002", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "XYZ789"},
            {"RP_DOCUMENT_ID": "DOC002", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "XYZ789"},
            {"RP_DOCUMENT_ID": "DOC003", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "XPTO50"}
        ]
        # Sample data with invalid RP_ENTITY_IDs
        self.sample_data_invalid_ids = [
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC002", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "XYZ789"},
            {"RP_DOCUMENT_ID": "DOC003", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "XPTO50"},
            {"RP_DOCUMENT_ID": "DOC004", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 2, "RP_ENTITY_ID": "ABC12"},    # Invalid: 5 characters
            {"RP_DOCUMENT_ID": "DOC005", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "1234567"},  # Invalid: 7 characters
            {"RP_DOCUMENT_ID": "DOC006", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 1, "RP_ENTITY_ID": "ABCD12X"}   # Invalid: 7 characters and non-alphanumeric
        ]
    
    def test_count_distinct_stories(self):
        count = count_distinct_stories(self.sample_data)
        self.assertEqual(count, 2)
    
    def test_find_missing_analytics_no_missing(self):
        missing_analytics = find_missing_analytics(self.sample_data)
        self.assertEqual(len(missing_analytics), 0)
    
    def test_find_missing_analytics_with_missing(self):
        missing_analytics = find_missing_analytics(self.sample_data_2)
        # Expect DOC001 to be missing index 3, and DOC003 to be missing index 1
        expected_missing = {
            "DOC001": [3],
            "DOC003": [1]
        }
        self.assertEqual(missing_analytics, expected_missing)
    
    def test_validate_entity_id(self):
        invalid_ids = validate_entity_id(self.sample_data_2)
        # Expect no invalid RP_ENTITY_IDs
        self.assertEqual(invalid_ids, [])
    
    def test_validate_invalid_entity_id(self):
        invalid_ids = validate_entity_id(self.sample_data_invalid_ids)
        # Expect to find invalid RP_ENTITY_IDs in the list
        expected_invalid_ids = [
            ("DOC004", "ABC12"), 
            ("DOC005", "1234567"), 
            ("DOC006", "ABCD12X")
        ]
        self.assertEqual(invalid_ids, expected_invalid_ids)


if __name__ == '__main__':
    unittest.main()
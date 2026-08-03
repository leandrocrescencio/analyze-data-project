import os
import tempfile
import unittest
from collections import defaultdict
from analyze_data import count_distinct_stories, find_missing_analytics, validate_entity_id, load_data

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
        self.sample_data__missing_indices = [
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
        missing_analytics = find_missing_analytics(self.sample_data__missing_indices)
        # Expect DOC001 to be missing index 3, and DOC003 to be missing index 1
        expected_missing = {
            "DOC001": [3],
            "DOC003": [1]
        }
        self.assertEqual(missing_analytics, expected_missing)
    
    def test_validate_entity_id(self):
        invalid_ids = validate_entity_id(self.sample_data__missing_indices)
        # Expect no invalid RP_ENTITY_IDs
        self.assertEqual(invalid_ids, {})
    
    def test_validate_invalid_entity_id(self):
        invalid_ids = validate_entity_id(self.sample_data_invalid_ids)
        # Expect to find invalid RP_ENTITY_IDs in the list
        # Expect DOC004  DOC005 and DOC006 to have invalid entity ids
        expected_invalid_ids = defaultdict(list, {
            "DOC004": ["ABC12"], 
            "DOC005": ["1234567"], 
            "DOC006": ["ABCD12X"]
    })
        self.assertEqual(invalid_ids, expected_invalid_ids)

    def test_find_missing_analytics_duplicate_index_does_not_mask_missing(self):
        # Regression test: DOC001 has a duplicated index (1 appears twice) and
        # is missing index 3, but len(indices) == DOCUMENT_RECORD_COUNT, so a
        # naive count comparison would previously skip it entirely.
        data_with_duplicate = [
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
            {"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 2, "DOCUMENT_RECORD_COUNT": 3, "RP_ENTITY_ID": "ABC123"},
        ]
        missing_analytics = find_missing_analytics(data_with_duplicate)
        self.assertEqual(missing_analytics, {"DOC001": [3]})


class TestLoadData(unittest.TestCase):

    def _write_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        temp_file.write(content)
        temp_file.close()
        self.addCleanup(os.remove, temp_file.name)
        return temp_file.name

    def test_load_data_missing_file_returns_empty_list(self):
        data = load_data('does_not_exist.json')
        self.assertEqual(data, [])

    def test_load_data_skips_malformed_json_line(self):
        content = (
            '{"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 1, "RP_ENTITY_ID": "ABC123"}\n'
            'not valid json\n'
        )
        filepath = self._write_temp_file(content)
        data = load_data(filepath)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['RP_DOCUMENT_ID'], 'DOC001')

    def test_load_data_skips_records_missing_required_fields(self):
        # Regression test: a record missing a required field (RP_ENTITY_ID here)
        # used to reach downstream functions and raise an unhandled KeyError,
        # aborting analysis for the whole file.
        content = (
            '{"RP_DOCUMENT_ID": "DOC001", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 1, "RP_ENTITY_ID": "ABC123"}\n'
            '{"RP_DOCUMENT_ID": "DOC002", "DOCUMENT_RECORD_INDEX": 1, "DOCUMENT_RECORD_COUNT": 1}\n'
        )
        filepath = self._write_temp_file(content)
        data = load_data(filepath)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['RP_DOCUMENT_ID'], 'DOC001')
        # Downstream functions must not raise despite the malformed input file
        count_distinct_stories(data)
        find_missing_analytics(data)
        validate_entity_id(data)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite([
        loader.loadTestsFromTestCase(TestAnalyzeData),
        loader.loadTestsFromTestCase(TestLoadData),
    ])
    unittest.TextTestRunner(verbosity=2).run(suite)

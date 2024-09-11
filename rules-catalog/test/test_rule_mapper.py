import unittest
from mappers.rule_mapper import validate_network_access_log, validate_rule

class TestMapEDRLogToLuluRule(unittest.TestCase):
    def test_validate_data_property(self):
        # Test with valid data
        valid_data = [
            {'causality_actor_process_image_path': '/path/to/image1', 'endpoints': {'192.168.1.1','host.com'}},
            {'causality_actor_process_image_path': '/path/to/image2', 'endpoints': {'192.168.1.1','host.com'}}
        ]
        self.assertTrue(validate_network_access_log(valid_data))

        # Test with invalid data
        invalid_data = [{'invalid_key': 'value'}]
        self.assertFalse(validate_network_access_log(invalid_data))

    def test_validate_lulu_rule(self):
        # Test with valid rule
        valid_rule = {
            'key': '/path/to/image1',
            'action': 'allow',
            'appLocation': '/path/to/image1',
            'endpoints': {'192.168.1.1','host.com'},
            'direction': 'outgoing'
            }
            
        self.assertTrue(validate_rule(valid_rule))

        invalid_rule = {'key': '/path/to/image1'}
        self.assertFalse(validate_rule(invalid_rule))


if __name__ == '__main__':

    unittest.main(verbosity=2, exit=False, argv=['', '-k', 'TestMapEDRLogToLuluRule'])

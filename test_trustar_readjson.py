#!/usr/bin/env python3.8
import unittest
from trustar_readjson import TrustarReadJson


class TestTrustarReadJson(unittest.TestCase):
    """
    Test class for the Trustar company challenge
    """

    def setUp(self):
        self.obj_trustar = TrustarReadJson()
        self.data = self.obj_trustar.read_json('test_data.json')

    def test_extract_valuable_information_arguments(self):
        properties_to_extract = 145
        self.assertRaises(TypeError, self.obj_trustar.extract_valuable_information,
                          self.data, properties_to_extract)

    def test_extract_valuable_information_data(self):
        properties_to_extract = [
            "guid", "content.entities", "score", "score.sign"]
        expected_result = {"guid": "1234", "content.entities": ["1.2.3.4", "wannacry",
                                                                "malware.com"], "score": 74}
        data = self.obj_trustar.extract_valuable_information(
            self.data, properties_to_extract)
        self.assertDictEqual(expected_result, data)

    def test_extract_valuable_information_accept_arbitrarily(self):
        properties_to_extract = "content.link.href.parent"
        data = self.obj_trustar.extract_valuable_information(
            self.data, properties_to_extract)
        self.assertDictEqual({}, data)

    def test_extract_valuable_acces_array(self):
        properties_to_extract = ["guid", "content.entities[0]"]
        expected_result = {"guid": "1234", "content.entities[0]": "1.2.3.4"}
        data = self.obj_trustar.extract_valuable_information(
            self.data, properties_to_extract)
        self.assertDictEqual(expected_result, data)

    def test_extract_valuable_acces_array_2(self):
        properties_to_extract = ["guid", "content.entities[0].time"]
        expected_result = {"guid": "1234"}
        data = self.obj_trustar.extract_valuable_information(
            self.data, properties_to_extract)
        self.assertDictEqual(expected_result, data)

    def test_extract_valuable_acces_array_2(self):
        properties_to_extract = ["guid", "content.entities[10]"]
        expected_result = {"guid": "1234"}
        data = self.obj_trustar.extract_valuable_information(
            self.data, properties_to_extract)
        self.assertDictEqual(expected_result, data)


if __name__ == '__main__':
    unittest.main()

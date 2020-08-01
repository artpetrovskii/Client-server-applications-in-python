import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_presence, process_answer

class TestClass(unittest.TestCase):
    def test_no_response(self):
        self.assertRaises(ValueError, process_answer, {ERROR: 'Bad Request'})

    def test_def_presence(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_answer_400(self):
        self.assertEqual(process_answer({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_answer_200(self):
        self.assertEqual(process_answer({RESPONSE: 200}), '200 : OK')

if __name__ == '__main__':
    unittest.main()

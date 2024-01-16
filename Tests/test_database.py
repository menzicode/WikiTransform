import unittest
from io import StringIO
import sys

# Import the Cython module you want to test
from WikiTransform.database import hello_cython


class TestHelloCython(unittest.TestCase):

    def test_hello_cython_output(self):
        # Capture the output of hello_cython
        capturedOutput = StringIO()          # Create StringIO object
        sys.stdout = capturedOutput          # Redirect stdout.
        hello_cython()                       # Call the function.
        sys.stdout = sys.__stdout__          # Reset redirect.

        # Now capturedOutput.getvalue() contains the stdout output of hello_cython()
        self.assertEqual(capturedOutput.getvalue().strip(),
                         "Hello from Cython!")


if __name__ == '__main__':
    unittest.main()

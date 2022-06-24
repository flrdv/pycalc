from unittest import TestSuite

from .testcases import evaluation_tests


full_suite = TestSuite()
full_suite.addTest(evaluation_tests)

# -*- coding: utf-8 -*- 
#!/usr/bin/env python
"""
Script run all unit tests in project.
"""
import unittest, sys

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner().run(all_tests)

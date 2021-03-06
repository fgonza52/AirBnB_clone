#!/usr/bin/python3
import unittest
import pep8
from inspect import getdoc, getmembers, isfunction
from datetime import datetime as dt
from models import base_model
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Super shiny documentation goes here.
    """
    def setUp(self):
        """Do this before each test."""
        self.m0 = BaseModel()

    def tearDown(self):
        """Clean up after yo'self."""
        del self.m0

    def test_docstring(self):
        """
        Test for docstrings at module, class, and function level
        """
        self.assertTrue(len(getdoc(base_model)) > 0, "Missing module docs")
        self.assertTrue(len(getdoc(BaseModel)) > 0, "Missing class docs")
        for _, fn in getmembers(BaseModel, isfunction):
            self.assertTrue(len(getdoc(fn)) > 0,
                            "Missing docs for {}".format(fn))

    def test_pep8(self):
        """
        Test pep8 conformance.
        https://pep8.readthedocs.io/en/release-1.7.x/advanced.html
        """
        file_msgs = [('models/base_model.py',
                      'Found code style errors in base_model.py.'),
                     ('tests/test_models/test_base_model.py',
                      'Found code style errors in test_base_model.py.')]
        for f, e in file_msgs:
            self.assertEqual(pep8.Checker(f).check_all(), 0, e)

    def test_unique_uuid(self):
        """Check that id's are unique."""
        m1 = BaseModel()
        self.assertNotEqual(self.m0.id, m1.id)

    def test_save(self):
        """Check that update_at gets *checks notes* updated?"""
        prev_time = self.m0.updated_at
        self.m0.save()
        self.assertNotEqual(prev_time, self.m0.updated_at)

    def test_str(self):
        """Checking __str__ magic method."""
        self.maxDiff = None
        self.assertEqual(str(self.m0), BaseModel._BaseModel__str_fmt
                         .format("BaseModel", self.m0.id, self.m0.__dict__))

    def test_to_dict(self):
        """Check your dict has the right class and attributes and types."""
        d = self.m0.to_dict()
        self.assertEqual(type(d), dict)
        self.assertTrue(hasattr(d, '__class__'))
        self.assertEqual(type(d['created_at']), str)
        self.assertEqual(type(d['updated_at']), str)

    def test_kwargs(self):
        """Test instantation with kwargs from json dictionary."""
        d = self.m0.to_dict()
        m1 = BaseModel(**d)
        self.assertEqual(self.m0.id, m1.id)
        self.assertEqual(self.m0.created_at, m1.created_at)
        self.assertEqual(self.m0.updated_at, m1.updated_at)
        self.assertNotEqual(self.m0, m1)

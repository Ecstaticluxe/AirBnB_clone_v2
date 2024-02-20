#!/usr/bin/python3
"""Test cases for HBNB console app"""
from models.engine.file_storage import FileStorage
import unittest
import cmd
import os
import json
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from unittest.mock import Mock
from models import storage
from models.base_model import BaseModel


class TestConsole(unittest.TestCase):
    """Test class for console"""
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Unsupported action")
    def test_create_default(self):
        """tests new create method"""
        with patch('sys.stdout', new=StringIO()) as mockout:
            HBNBCommand().onecmd('create State name="Central"')
            output = mockout.getvalue().strip()
            key = 'State.{}'.format(output)
            self.assertIn(key, storage.all().keys())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Unsupported action")
    def test_create_multiple_args(self):
        """tests new create method with multiple arguments passed"""
        with patch('sys.stdout', new=StringIO()) as mockout:
            HBNBCommand().onecmd('create User name="Hamida" age=23 height=5.3')
            output = mockout.getvalue().strip()
            key = 'User.{}'.format(output)
            self.assertIn(key, storage.all().keys())

            HBNBCommand().onecmd('show User {}'.format(output))
            self.assertIn("'name': 'Hamida'", mockout.getvalue().strip())
            self.assertIn("height': 5.3", mockout.getvalue().strip())
            self.assertIn("'age': 23", mockout.getvalue().strip())

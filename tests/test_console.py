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

class TestCreateCommand(unittest.TestCase):
    def setUp(self):
        """Set up the test"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tear down the test"""
        del self.console

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_valid_input(self, mock_stdout):
        """Test create command with valid input"""
        with patch('builtins.input', side_effect=['create BaseModel name="test"', 'EOF']):
            self.console.cmdloop()

        output = mock_stdout.getvalue().strip()
        self.assertIn("test", output)  # Check if the object is created

        # Clean up created objects
        del storage.all()["BaseModel.test"]

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_invalid_class(self, mock_stdout):
        """Test create command with invalid class name"""
        with patch('builtins.input', side_effect=['create InvalidClass name="test"', 'EOF']):
            self.console.cmdloop()

        output = mock_stdout.getvalue().strip()
        self.assertIn("** class doesn't exist **", output)  # Check for error message

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_missing_class_name(self, mock_stdout):
        """Test create command with missing class name"""
        with patch('builtins.input', side_effect=['create', 'EOF']):
            self.console.cmdloop()

        output = mock_stdout.getvalue().strip()
        self.assertIn("** class name missing **", output)  # Check for error message

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_missing_parameters(self, mock_stdout):
        """Test create command with missing parameters"""
        with patch('builtins.input', side_effect=['create BaseModel', 'EOF']):
            self.console.cmdloop()

        output = mock_stdout.getvalue().strip()
        self.assertIn("** parameters missing **", output)  # Check for error message

if __name__ == '__main__':
    unittest.main()

import os
import json
import unittest
from unittest.mock import patch
from io import StringIO
from click.testing import CliRunner
from codarcane.your_script import load_snippets, save_snippets, export_as_markdown, export_as_text, cli


class TestYourScriptFunctions(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = 'temp_test_dir'
        os.makedirs(self.temp_dir, exist_ok=True)

        # Set the JSON file path to the temporary directory
        self.json_file_path = os.path.join(self.temp_dir, 'snippets.json')

        # Create a runner to invoke Click commands
        self.runner = CliRunner()

    def tearDown(self):
        # Remove the temporary directory after testing
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))

    def test_load_snippets(self):
        # Test if the function can load snippets from a JSON file
        snippets_data = [{"title": "Test Title",
                          "language": "Test Language", "code": "Test Code"}]
        with open(self.json_file_path, 'w') as f:
            json.dump(snippets_data, f)
        loaded_snippets = load_snippets()
        self.assertEqual(loaded_snippets, snippets_data)

    def test_save_snippets(self):
        # Test if the function can save snippets to a JSON file
        snippets_data = [{"title": "Test Title",
                          "language": "Test Language", "code": "Test Code"}]
        save_snippets(snippets_data)
        with open(self.json_file_path, 'r') as f:
            saved_snippets = json.load(f)
        self.assertEqual(saved_snippets, snippets_data)

    @patch('sys.stdout', new_callable=StringIO)
    def test_export_as_markdown(self, mock_stdout):
        # Test if the function can export snippets as Markdown
        snippets_data = [{"title": "Test Title",
                          "language": "Test Language", "code": "Test Code"}]
        expected_output = "**Title:** Test Title\n**Language:** Test Language\n```\nTest Code\n```\n\n"
        export_as_markdown(snippets_data, sys.stdout)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_export_as_text(self, mock_stdout):
        # Test if the function can export snippets as plain text
        snippets_data = [{"title": "Test Title",
                          "language": "Test Language", "code": "Test Code"}]
        expected_output = "Title: Test Title\nLanguage: Test Language\nCode:\nTest Code\n\n"
        export_as_text(snippets_data, sys.stdout)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_add_command(self):
        # Test the 'add' command using the Click runner
        result = self.runner.invoke(
            cli, ['add'], input='Test Title\nTest Language\nTest Code\n')
        self.assertTrue(result.output.startswith(
            'Snippet added successfully!'))

    # ... (similar adjustments for other test cases)


if __name__ == '__main__':
    unittest.main()

import sys
import os
import csv
import logging

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from yt_to_vimeo.yt_to_vimeo import write_url_mapping
@pytest.fixture(autouse=True)
def caplog_config(caplog):
    caplog.set_level(logging.INFO)

class TestWriteUrlMapping:

    # Successfully writes a new mapping to an existing file
    def test_successfully_writes_new_mapping(self, tmp_path):
        source_url = "http://example.com/source"
        destination_url = "http://example.com/destination"
        path = tmp_path

        # Create an existing file
        file_path = os.path.join(path, 'url_mapping.csv')
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["existing_source", "existing_destination"])

        write_url_mapping(source_url, destination_url, path)

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        assert rows == [["existing_source", "existing_destination"], [source_url, destination_url]]

    # Creates a new file if it doesn't exist and writes the mapping
    def test_creates_new_file_and_writes_mapping(self, tmp_path):  
        source_url = "http://example.com/source"
        destination_url = "http://example.com/destination"
        path = tmp_path

        write_url_mapping(source_url, destination_url, path)

        file_path = os.path.join(path, 'url_mapping.csv')
        assert os.path.exists(file_path)

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        assert rows == [[source_url, destination_url]]

    # Handles file path with insufficient permissions
    def test_handles_insufficient_permissions(self, tmp_path, caplog):
        source_url = "http://example.com/source"
        destination_url = "http://example.com/destination"
        path = tmp_path

        # Create a file with insufficient permissions
        file_path = os.path.join(path, 'url_mapping.csv')
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["existing_source", "existing_destination"])

        # Change file permissions to read-only
        os.chmod(file_path, 0o444)

        write_url_mapping(source_url, destination_url, path)

        assert f'Error writing to file {file_path}' in caplog.text

        # Handles read-only file system scenarios
    def test_handles_read_only_file_system(self, tmp_path, caplog):
        source_url = "http://example.com/source"
        destination_url = "http://example.com/destination"
        path = tmp_path

        # Create a file with read-only permissions
        file_path = os.path.join(path, 'url_mapping.csv')
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["existing_source", "existing_destination"])

        # Change file permissions to read-only
        os.chmod(file_path, 0o444)

        write_url_mapping(source_url, destination_url, path)

        assert f'Error writing to file {file_path}' in caplog.text
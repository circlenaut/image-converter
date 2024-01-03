import pytest
from pathlib import Path
from unittest.mock import MagicMock

from image_converter.app import ImageConverter

TEST_ROOT_FOLDER_ID = '1JuP3YAZyl0OHXqfqmcv4bN1thhfvSBFM'
TEST_LOCAL_ROOT_FOLDER = 'test_result'

class TestRunConversion:

    # raises FileNotFoundError if credentials.json file is missing
    def test_raises_file_not_found_error_missing_credentials(self, mocker):
        # Mock the necessary dependencies
        mocker.patch('builtins.input', return_value='y')
        mocker.patch('image_converter.app.ImageConverter.count_files', return_value=10)
        mocker.patch('image_converter.app.tqdm')

        # Mock to raise FileNotFoundError for credentials and default credentials
        mocker.patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file', side_effect=FileNotFoundError)
        mocker.patch('google.oauth2.credentials.Credentials.from_authorized_user_file', side_effect=FileNotFoundError)

        # Mock Path.exists to return False for token.pickle
        mocker.patch.object(Path, 'exists', return_value=False)

        # Assert that FileNotFoundError is raised during initialization of ImageConverter
        with pytest.raises(FileNotFoundError):
            converter = ImageConverter(TEST_ROOT_FOLDER_ID, TEST_LOCAL_ROOT_FOLDER, format='png')

    def test_raises_value_error(self, mocker):
        # Mock the necessary dependencies
        mocker.patch('builtins.input', return_value='y')
        mocker.patch('image_converter.app.ImageConverter.count_files', return_value=10)
        mocker.patch('image_converter.app.tqdm')

        # Create an instance of ImageConverter with an invalid format
        with pytest.raises(ValueError):
            converter = ImageConverter(TEST_ROOT_FOLDER_ID, TEST_LOCAL_ROOT_FOLDER, format='invalid_format')

    # raises FileNotFoundError if root folder ID is invalid
    def test_raises_file_not_found_error_invalid_folder_id(self, mocker):
        # Mock the necessary dependencies
        mocker.patch('builtins.input', return_value='y')
        mocker.patch('image_converter.app.ImageConverter.count_files', side_effect=FileNotFoundError)
        mocker.patch('image_converter.app.tqdm')

        # Create an instance of ImageConverter
        converter = ImageConverter(TEST_ROOT_FOLDER_ID, TEST_LOCAL_ROOT_FOLDER, format='png')

        # Call the run_conversion method and assert that FileNotFoundError is raised
        with pytest.raises(FileNotFoundError):
            converter.run_conversion()
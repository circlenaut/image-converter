import logging
import pickle
from pathlib import Path

import fire
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tqdm import tqdm

from image_converter.heic import download_and_convert as download_and_convert_heic

SCOPES = ['https://www.googleapis.com/auth/drive']

class ImageConverter:
    def __init__(self, root_folder_id, local_root_folder, verbose=False, format='png'):
        self.root_folder_id = root_folder_id
        self.local_root_folder = Path(local_root_folder)
        self.verbose = verbose
        self.setup_logging()
        self.service = self.authenticate_google_drive()

        self.valid_formats = ['png', 'jpg', 'jpeg']  # Define valid formats
        if format.lower() not in self.valid_formats:
            raise ValueError(f"Invalid format '{format}'. Valid formats are: {', '.join(self.valid_formats)}")
        self.format = format.lower()

    def setup_logging(self):
        level = logging.DEBUG if self.verbose else logging.WARNING
        logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    def authenticate_google_drive(self):
        creds = None
        token_path = Path('token.pickle')
        if token_path.exists():
            creds = pickle.load(token_path.open('rb'))

        if not creds or not creds.valid:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                pickle.dump(creds, token_path.open('wb'))
            except FileNotFoundError:
                creds = Credentials.from_authorized_user_file('default_credentials.json', SCOPES)
                logging.warning("Using default credentials")

        return build('drive', 'v3', credentials=creds)

    def count_files(self, folder_id):
        query = f"'{folder_id}' in parents"
        items = self.service.files().list(q=query).execute().get('files', [])
        return sum(1 if item['mimeType'] != 'application/vnd.google-apps.folder' else self.count_files(item['id']) for item in items)

    def download_and_convert_images(self, folder_id, progress, relative_path=Path()):
        query = f"'{folder_id}' in parents"
        items = self.service.files().list(q=query).execute().get('files', [])

        for item in items:
            current_relative_path = relative_path / item['name']
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                local_folder_path = self.local_root_folder / current_relative_path
                local_folder_path.mkdir(parents=True, exist_ok=True)
                self.download_and_convert_images(item['id'], progress, current_relative_path)
            else:
                self.process_file(item, current_relative_path)
                progress.update(1)

    def process_file(self, item, current_relative_path):
        file_id = item['id']
        if current_relative_path.suffix.lower() == '.heic':
            image = download_and_convert_heic(self.service, file_id, self.format)
            output_path = (self.local_root_folder / current_relative_path).with_suffix(f'.{self.format}')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path)
            logging.debug(f"Converted {current_relative_path} to {output_path}")

    def run_conversion(self):
        if self.local_root_folder.exists():
            user_input = input(f"The directory '{self.local_root_folder}' already exists. Overwrite? (y/n): ")
            if user_input.lower() != 'y':
                logging.warning("Operation cancelled by the user.")
                return

        total_file_count = self.count_files(self.root_folder_id)
        try:
            with tqdm(total=total_file_count, desc="Overall Progress") as progress:
                self.download_and_convert_images(self.root_folder_id, progress)
        except KeyboardInterrupt:
            logging.warning('Process interrupted by user. Exiting.')

def run():
    fire.Fire(lambda root_folder_id, local_root_folder, verbose=False, format='png': 
              ImageConverter(root_folder_id, local_root_folder, verbose, format).run_conversion())

if __name__ == '__main__':
    run()
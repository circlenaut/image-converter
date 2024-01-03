import io

import pyheif
from PIL import Image

from googleapiclient.http import MediaIoBaseDownload

def convert_heic_to(fh, format):
    """Converts HEIC file handle to specified format using Pillow."""
    heif_file = pyheif.read(fh)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride)
    return image

def download_and_convert(service, file_id, format):
    """Downloads and converts HEIC file to specified format."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    return convert_heic_to(fh, format)

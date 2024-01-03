# Image Converter

Image Converter is a Python-based tool that simplifies the process of converting HEIC image files to other formats such as PNG, JPG, or JPEG. Utilizing Google Drive API, this tool enables users to download HEIC files from Google Drive, convert them to a desired format, and save them locally.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project aims to provide a seamless solution for converting HEIC images stored in Google Drive to more widely supported formats like PNG and JPG. It's particularly useful for users who frequently deal with HEIC files and need an efficient way to convert and manage these images.

## Features

- **Google Drive Integration**: Connects to Google Drive to access and download HEIC files.
- **Multiple Format Support**: Converts images to popular formats such as PNG, JPG, and JPEG.
- **Batch Conversion**: Processes multiple files at once, saving time and effort.
- **Progress Tracking**: Displays a progress bar for tracking the conversion process.
- **Customizable Output Directory**: Allows users to specify a local directory for saving converted images.
- **Verbose Logging**: Offers an optional verbose mode for detailed logging information.

## Prerequisites (Ubuntu)

Before installing and running the Image Converter, make sure your system has the necessary dependencies. Run the following commands on Ubuntu to install them:

1. Update and upgrade the system packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
    ```
2. Add the DeadSnakes PPA for Python 3.10:
    ```bash
    sudo add-apt-repository ppa:deadsnakes/ppa
    ```
3. Install Python 3.10 and development headers:
    ```bash
    sudo apt install python3.10 python3.10-dev
    ```
4. Install the HEIF library development files:
    ```bash
    sudo apt-get install libheif-dev libde265-0 libheif1
    ```

Ensure these steps are completed before proceeding with the installation of the Image Converter.

## Installation

To install Image Converter, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com:circlenaut/image-converter.git
   ```
2. Navigate to the cloned directory:
    ```bash
    cd image-converter
    ```
3. Install the required packages using Poetry:
    ```bash
    poetry install
    ```

## Usage

To use Image Converter, run the following command:
```bash
poetry run convert --root_folder_id <Google Drive Folder ID> --local_root_folder <Local Directory> [--verbose] [--format <png|jpg|jpeg>]
```

### Parameters
- **--root_folder_id**: ID of the Google Drive folder containing HEIC files.
- **--local_root_folder**: Path to the local directory where converted images will be saved.
- **--verbose (optional)**: Enables verbose logging.
- **--format (optional)**: Specifies the output format (default is 'png').

### Example
```bash
poetry run convert --root_folder_id 1JuP3YAZyl0OHXqfqmcv4bN1thhfvSBFM --local_root_folder ./converted-images --format jpg
```

### Dependencies
- Python 3.10
- Google Drive API
- Pillow
- PyHeif
- tqdm
- fire
- pytest-mock

For a full list of dependencies, refer to pyproject.toml.

## Testing

### Running Tests

To ensure the quality and functionality of the Image Converter, a suite of tests has been provided. To run these tests, follow these steps:

1. Navigate to the project's root directory.
2. Run the tests using Poetry:
   ```bash
   poetry run pytest
    ```

This command will execute all the tests and provide a report on their success or failure.

### Test Coverage

The tests aim to cover the following aspects of the application:

- **Functionality Testing**: Ensuring that each function behaves as expected under various conditions.
- **Error Handling**: Verifying that the application correctly handles and reports errors, such as missing files or incorrect input formats.
- **Integration Testing**: Testing the integration between different components of the application, such as downloading files from Google Drive and converting them.

### Adding Tests

Contributors are encouraged to add tests when proposing new features or fixing bugs. To add a test:

1. Write your tests in the `tests` directory.
2. Ensure your tests are well-documented and clear in their purpose.
3. Run the test suite to ensure your new tests and existing ones pass successfully.

By maintaining a robust suite of tests, we can collectively ensure the reliability and stability of the Image Converter.


## Contributing

Contributions to Image Converter are welcome. To contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes and push them to your branch.
4. Submit a pull request.

For bug reports or feature requests, please open an issue.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries or support, please contact Phillip Strefling at phillip@mindblox.xyz.

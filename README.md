# File Organizer App

A Python desktop application that automatically organizes files in a directory based on their file extensions. The app features both dark and light modes for user preference.

## Features

- **Automatic File Organization**: Sorts files into appropriate folders based on file type
- **Dark/Light Mode**: Toggle between themes with a single click
- **User-Friendly Interface**: Simple and intuitive GUI built with tkinter
- **Progress Tracking**: Real-time progress bar and detailed operation log
- **File Categorization**: Automatically categorizes files into folders like:
  - Images (jpg, png, gif, etc.)
  - Videos (mp4, mov, avi, etc.)
  - Music (mp3, wav, flac, etc.)
  - Documents (doc, pdf, xls, ppt, etc.)
  - Archives (zip, rar, 7z, etc.)
  - Code Files (py, java, html, etc.)
  - And more!

## Installation

### Prerequisites

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)

### Steps

1. Clone this repository or download the source code:
   ```
   git clone https://github.com/nicatbayram/file-organizer.git
   ```
2. Navigate to the project directory:
   ```
   cd file-organizer
   ```
3. Run the application:
   ```
   python main.py
   ```

## Usage

1. Launch the application
2. Select a directory to organize by clicking the "Browse" button
3. Click "Organize Files" to start the organization process
4. Monitor progress in the log area
5. Once complete, your files will be neatly organized into appropriate folders

## Customization

You can easily customize the file organization rules by editing the `get_folder_name` method in the source code. This allows you to:

- Add support for additional file extensions
- Change folder naming conventions
- Create custom categorization rules

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Open a Pull Request

## Acknowledgements

- Thanks to the Python and tkinter communities for their excellent documentation
- Icons provided by [Lucide Icons](https://lucide.dev/)

## ScreenShots

<img width="420" alt="1" src="https://github.com/user-attachments/assets/8685a9a8-8e41-428b-9cf9-2fb35030ef6c" />
<img width="420" alt="2" src="https://github.com/user-attachments/assets/fa9ae6bc-149c-4e3b-bbfc-764e4d5e9eff" />


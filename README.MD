# File Manager Application 📂📄📈

## Overview

This is a Python-based file management application developed using the Flet framework. The application allows users to organize files in a specified directory into categorized folders based on their file extensions. It also provides functionalities to add custom folders with specific file extensions, create backups before organizing, and generate a summary of the file types and their sizes.

## Features

- **Select Source Directory**: Choose the directory containing the files to be organized.
- **Default Folder Categories**: Predefined categories for Music, Photos, Documents, and Videos.
- **Add Custom Folders**: Add custom folders with specific file extensions.
- **Organize Files**: Move files to appropriate folders based on their extensions.
- **Backup Functionality**: Create a backup of the source directory before organizing.
- **Summary Report**: Generate and display a summary of file types and their sizes.
- **Plot Summary**: Visual representation of the summary report using a bar chart.

## Requirements

The application requires the following Python packages:

- flet==0.22.1
- matplotlib==3.9.0
- numpy==1.26.4
- pytest==8.2.1
- darkdetect==0.8.0

To install these packages, use the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. **Cloning the Repository**:
   First, clone the repository using Git:

   ```bash
   git clone https://github.com/Celestial-0/FILE-MANAGER.git
   cd FILE-MANAGER
   ```

2. **Installing Dependencies**:
   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Running the Application**:
   To start the application, execute the `project.py` script:

   ```bash
   python project.py
   ```

4. **User Interface**:
   - **Source Directory**: Select the source directory using the "Select Source Directory" button.
   - **Default Folders**: The application includes default folder names for Music, Photos, Documents, and Videos. These can be customized.
   - **Custom Folders**: Add custom folders by specifying the folder name and associated file extensions.
   - **Organize Files**: Click the "Organize Files" button to start organizing files. The application will create a backup, organize files, and display a summary report.
   - **Summary and Plot**: The summary report is displayed in a text field, and a bar chart representing the summary is shown in an image field.

5. **Logs**:
   - The application logs its activities in a log file named `file_manager.log`.

### Working and Details

<!-- markdownlint-disable-next-line MD033 -->
<iframe width="1473" height="621" src="https://www.youtube.com/embed/N5y7y4f_V-g" title="FILE-MANAGER 📂📄📈" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Screenshot of the File Manager Application

![Screenshot of the application](./assets/ss/Screenshot%202024-05-22%20071713.png)

## Example UseCases

- **Test Folder**

![Test Folder](./assets/ss/Screenshot%202024-05-22%20071820.png)

- **App after Initiated**

![Result(App)](./assets/ss/Screenshot%202024-05-22%20071902.png)

- **Result App Folder**

![Result(Folder(Test))](./assets/ss/Screenshot%202024-05-22%20071908.png)

- **Log File**

[Log File](./assets/ss/file_manager.log)

## Code Structure

- **project.py**: Contains the project application code including the user interface and file organization logic.
- **requirements.txt**: Lists the required Python packages.

## Key Functions

- **`FileManagerApp.__init__(self, page: ft.Page)`**: Initializes the application with UI components and default settings.
- **`FileManagerApp.init_ui(self)`**: Sets up the user interface components.
- **`FileManagerApp.get_folders(self)`**: Retrieves the folder names and associated file extensions.
- **`FileManagerApp.create_dirs(self, base_dir, folders)`**: Creates necessary directories for organizing files.
- **`FileManagerApp.move_file(self, file, base_dir, folders)`**: Moves a file to the appropriate folder.
- **`FileManagerApp.organize_files(self, src_dir, folders)`**: Organizes files in the source directory.
- **`FileManagerApp.backup_files(self, src_dir)`**: Creates a backup of the source directory.
- **`FileManagerApp.summarize_files(self, src_dir)`**: Summarizes the file types and their sizes in the source directory.
- **`FileManagerApp.format_summary(self, file_sizes)`**: Formats the summary of file sizes for display.
- **`FileManagerApp.plot_summary(self, file_sizes)`**: Generates a bar chart of the file sizes summary.
- **`FileManagerApp.on_pick_src_click(self, e)`**: Callback for selecting the source directory.
- **`FileManagerApp.on_add_custom_click(self, e)`**: Callback for adding a custom folder.
- **`FileManagerApp.on_organize_click(self, e)`**: Callback for organizing files.
- **`FileManagerApp.on_pick_result(self, result: ft.FilePickerResultEvent)`**: Callback for handling the result of directory selection.
- **`FileManagerApp.show_error_dialog(self, message)`**: Displays an error dialog with the specified message.

## Author

Developed by YASH

## License

This project is licensed under the MIT License.

---

Feel free to explore and modify the application as per your requirements. If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request on the project's repository.

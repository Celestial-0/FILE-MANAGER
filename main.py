import os
import shutil
import logging
from datetime import datetime
import flet as ft
import matplotlib.pyplot as plt
import numpy as np

from config import DEFAULT_FOLDERS

logging.basicConfig(filename='file_manager.log', level=logging.INFO)

plt.switch_backend('Agg')


class FileManagerApp:
    """A file management application."""
    
    def __init__(self, page: ft.Page):
        """
        Initializes the FileManagerApp.

        Args:
            page (ft.Page): The Flet page to display the application.
        """
        self.page = page
        self.page.title = "File Manager"
        self.page.window_width = 1280
        self.page.window_height = 760
        self.page.window_min_width = 1280
        self.page.window_min_height = 760
        self.page.window_resizable = True
        self.page.window_icon = "./assets/icon1.png"

        self.init_ui()

        self.custom_folders = []

        # Initialize FilePicker
        self.file_picker = ft.FilePicker(on_result=self.on_pick_result)
        self.page.overlay.append(self.file_picker)
        self.page.update()

    def init_ui(self):
        """Initializes the UI components."""
        self.src_dir_input = ft.TextField(label="Source Directory", width=300, read_only=True)
        self.pick_src_button = ft.ElevatedButton(
            text="Select Source Directory",
            on_click=self.on_pick_src_click,
            icon=ft.icons.FOLDER_OPEN,
            color=ft.colors.BLUE
        )

        self.music_input = ft.TextField(label="Custom Music Folder", width=300, value="Music")
        self.photos_input = ft.TextField(label="Custom Photos Folder", width=300, value="Photos")
        self.docs_input = ft.TextField(label="Custom Documents Folder", width=300, value="Documents")
        self.videos_input = ft.TextField(label="Custom Videos Folder", width=300, value="Videos")

        self.custom_folder_input = ft.TextField(label="Custom Folder Name", width=300)
        self.custom_exts_input = ft.TextField(label="File Extensions (comma-separated)", width=300)
        self.add_custom_button = ft.ElevatedButton(
            text="Add Custom Folder",
            on_click=self.on_add_custom_click,
            icon=ft.icons.ADD,
            color=ft.colors.GREEN
        )

        self.custom_list = ft.Column()
        self.organize_button = ft.ElevatedButton(
            text="Organize Files",
            on_click=self.on_organize_click,
            icon=ft.icons.SORT,
            color=ft.colors.PURPLE
        )
        self.summary_input = ft.TextField(
            label="Summary After Organize",
            multiline=True,
            width=300,
            height=200,
            read_only=True
        )
        self.progress_bar = ft.ProgressBar(width=300)
        self.progress_bar.visible = False
        
        self.plot_image = ft.Image(width=600, height=400, src="Nothing", fit=ft.ImageFit.CONTAIN)
        self.author_mark = ft.Text("Developed by YASH", size=12, color=ft.colors.GREY)
        self.author_row = ft.Row([self.author_mark], alignment=ft.MainAxisAlignment.CENTER)

        self.page.add(
            ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Column([self.src_dir_input, self.pick_src_button]),
                        ft.Divider(),
                        self.music_input,
                        self.photos_input,
                        self.docs_input,
                        self.videos_input,
                        ft.Divider(),
                        ft.Text("Add Custom Folder"),
                        self.custom_folder_input,
                        self.custom_exts_input,
                        self.add_custom_button,
                        self.custom_list,
                        ft.Divider(),
                    ], scroll=ft.ScrollMode.ALWAYS),
                    self.plot_image,
                    ft.Column([
                        self.organize_button,
                        self.progress_bar,
                        self.summary_input,
                    ]),
                ], scroll=ft.ScrollMode.ALWAYS),
                self.author_row,
            ], scroll=ft.ScrollMode.ALWAYS, alignment=ft.MainAxisAlignment.CENTER)
        )

    def get_folders(self):
        """Retrieve folder names for each file type."""
        folders = {self.music_input.value: DEFAULT_FOLDERS['Music'],
                   self.photos_input.value: DEFAULT_FOLDERS['Photos'],
                   self.docs_input.value: DEFAULT_FOLDERS['Docs'],
                   self.videos_input.value: DEFAULT_FOLDERS['Videos']}
        for folder_name, folder_exts in self.custom_folders:
            folders[folder_name] = folder_exts
        folders["Others"] = []
        return folders

    def create_dirs(self, base_dir, folders):
        """Create folders for each file type if they don't exist."""
        for folder in folders.keys():
            folder_path = os.path.join(base_dir, folder)
            if not os.path.exists(folder_path):
                try:
                    os.makedirs(folder_path)
                    logging.info(f"Created folder: {folder_path}")
                except Exception as e:
                    logging.error(f"Error creating folder {folder_path}: {e}")
                    self.show_error_dialog(f"Error creating folder {folder_path}: {e}")

    def move_file(self, file, base_dir, folders):
        """Move a file to the appropriate folder based on its extension."""
        try:
            file_ext = file.split('.')[-1].lower()
            moved = False
            for folder, exts in folders.items():
                if file_ext in exts:
                    dest_folder = os.path.join(base_dir, folder)
                    shutil.move(os.path.join(base_dir, file), dest_folder)
                    logging.info(f"Moved file: {file} to {dest_folder}")
                    moved = True
                    break
            if not moved:
                others_folder = os.path.join(base_dir, "Others")
                shutil.move(os.path.join(base_dir, file), others_folder)
                logging.info(f"Moved file: {file} to {others_folder}")
        except Exception as e:
            logging.error(f"Error moving file {file}: {e}")
            self.show_error_dialog(f"Error moving file {file}: {e}")

    def organize_files(self, src_dir, folders):
        """Organize files in the source directory into specific folders."""
        self.create_dirs(src_dir, folders)
        for file in os.listdir(src_dir):
            file_path = os.path.join(src_dir, file)
            if os.path.isfile(file_path):
                self.move_file(file, src_dir, folders)

    def backup_files(self, src_dir):
        """Backup files in the source directory before organizing."""
        try:
            backup_dir = os.path.join(src_dir, 'backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
            shutil.copytree(src_dir, backup_dir)
            logging.info(f"Backup created at: {backup_dir}")
            return backup_dir
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            self.show_error_dialog(f"Error creating backup: {e}")
            return None

    def summarize_files(self, src_dir):
        """Provide a summary of the file types and their counts."""
        file_sizes = {}
        logging.info(f"Summarizing files in directory: {src_dir}")
        
        for root, _, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_ext = os.path.splitext(file)[1].lower()
                    file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                    if file_ext in file_sizes:
                        file_sizes[file_ext] += file_size
                    else:
                        file_sizes[file_ext] = file_size

        logging.info(f"File sizes summary: {file_sizes}")
        return file_sizes

    def format_summary(self, file_sizes):
        """Format the summary of file sizes for display."""
        sorted_files = sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)
        formatted_summary = "In order of size of each type of file:\n"
        for ext, size in sorted_files:
            formatted_summary += f"{ext.upper()[1:]}: {size:.1f}MB\n"
        return formatted_summary

    def plot_summary(self, file_sizes):
        """Plot the summary of file sizes and save it as an image file."""
        extensions = list(file_sizes.keys())
        sizes = list(file_sizes.values())
        colors = plt.cm.tab20c(np.linspace(0, 1, len(extensions)))

        fig, ax = plt.subplots(facecolor='black')
        bars = ax.bar(extensions, sizes, color=colors)

        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.set_xlabel("File Types", color='white')
        ax.set_ylabel("Size (MB)", color='white')
        ax.set_title("File Sizes by Type", color='white')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.1f}MB', ha='center', color='white')

        plt.tight_layout()

        plot_file = "file_sizes_summary.png"
        plt.savefig(plot_file, facecolor=fig.get_facecolor())
        plt.close(fig)

        return plot_file

    def on_pick_src_click(self, e):
        """Callback for selecting the source directory."""
        self.file_picker.get_directory_path()

    def on_add_custom_click(self, e):
        """Callback for adding a custom folder."""
        folder_name = self.custom_folder_input.value
        folder_exts = [ext.strip().lower() for ext in self.custom_exts_input.value.split(',')]
        if folder_name and folder_exts:
            self.custom_folders.append((folder_name, folder_exts))
            self.custom_list.controls.append(ft.Text(f"{folder_name}: {', '.join(folder_exts)}"))
            self.custom_folder_input.value = ""
            self.custom_exts_input.value = ""
            self.page.update()
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Success"),
                content=ft.Text(f"Added custom folder {folder_name} with extensions: {', '.join(folder_exts)}")
            )
            self.page.dialog.open = True
            self.page.update()
        else:
            self.show_error_dialog("Please provide both folder name and extensions.")

    def on_organize_click(self, e):
        """Callback for organizing files."""
        src_dir = self.src_dir_input.value
        if os.path.isdir(src_dir):
            folders = self.get_folders()
            self.progress_bar.visible = True
            self.page.update()
            backup_dir = self.backup_files(src_dir)
            if backup_dir:
                try:
                    self.organize_files(src_dir, folders)
                    file_sizes = self.summarize_files(src_dir)
                    summary_text = self.format_summary(file_sizes)
                    self.summary_input.value = summary_text
                    plot_file = self.plot_summary(file_sizes)
                    if plot_file and os.path.exists(plot_file):
                        self.plot_image.src = plot_file
                    else:
                        self.plot_image.alt = "Nothing"
                    self.plot_image.update()
                    self.page.update()
                except Exception as e:
                    logging.error(f"Error organizing files: {e}")
                    self.show_error_dialog(f"Error organizing files: {e}")
            self.progress_bar.visible = False
            self.page.update()
        else:
            self.show_error_dialog(f"Directory {src_dir} does not exist.")

    def on_pick_result(self, result: ft.FilePickerResultEvent) -> None:
        """Callback for picking a directory using FilePicker."""
        if result and result.path:
            if os.path.isdir(result.path):
                self.src_dir_input.value = result.path
                self.page.update()
            else:
                self.show_error_dialog("Please select a valid directory.")
        else:
            self.show_error_dialog("No directory selected.")

    def show_error_dialog(self, message):
        """Show an error dialog with the specified message."""
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message)
        )
        self.page.dialog.open = True
        self.page.update()


def main(page: ft.Page):
    """Main function to start the application."""
    FileManagerApp(page)


if __name__ == "__main__":
    ft.app(target=main)

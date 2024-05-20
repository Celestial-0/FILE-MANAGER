import os
import pytest
from unittest import mock
from main import FileManagerApp
from flet import Page, Text
from config import DEFAULT_FOLDERS

# Helper function to create a mock Page
def create_mock_page():
    mock_page = mock.MagicMock(spec=Page)
    return mock_page

@pytest.fixture
def app():
    mock_page = create_mock_page()
    return FileManagerApp(mock_page)

def test_get_folders(app):
    # Default folders plus custom folders
    expected_folders = DEFAULT_FOLDERS.copy()
    expected_folders.update({
        "Others": []
    })
    assert app.get_folders() == expected_folders

def test_create_dirs(tmpdir, app):
    base_dir = tmpdir.mkdir("test_dir")
    folders = {"Music": [], "Photos": []}
    app.create_dirs(base_dir, folders)
    assert os.path.exists(os.path.join(base_dir, "Music"))
    assert os.path.exists(os.path.join(base_dir, "Photos"))

def test_move_file(tmpdir, app):
    base_dir = tmpdir.mkdir("test_dir")
    music_dir = base_dir.mkdir("Music")
    others_dir = base_dir.mkdir("Others")
    
    test_file = base_dir.join("test.mp3")
    test_file.write("dummy content")
    
    folders = {"Music": ["mp3"], "Others": []}
    app.move_file("test.mp3", base_dir, folders)
    
    assert os.path.exists(os.path.join(music_dir, "test.mp3"))
    assert not os.path.exists(os.path.join(base_dir, "test.mp3"))

def test_summarize_files(tmpdir, app):
    base_dir = tmpdir.mkdir("test_dir")
    test_file_1 = base_dir.join("test1.mp3")
    test_file_2 = base_dir.join("test2.mp3")
    test_file_3 = base_dir.join("test.txt")

    # Write exact number of bytes to match expected sizes
    test_file_1.write(b"a" * int(10.5 * 1024 * 1024))  # 10.5MB
    test_file_2.write(b"a" * int(5.25 * 1024 * 1024))  # 5.25MB
    test_file_3.write(b"a" * int(1 * 1024 * 1024))     # 1MB

    file_sizes = app.summarize_files(base_dir)
    # Check that file sizes are approximately equal to the expected sizes.
    assert pytest.approx(file_sizes['.mp3'], rel=0.01) == 15.75
    assert pytest.approx(file_sizes['.txt'], rel=0.01) == 1.0

def test_on_pick_src_click(app):
    with mock.patch.object(app.file_picker, 'get_directory_path') as mock_picker:
        app.on_pick_src_click(None)
        mock_picker.assert_called_once()

def test_on_add_custom_click(app):
    app.custom_folder_input.value = "CustomFolder"
    app.custom_exts_input.value = "custom"

    with mock.patch.object(app.page, 'update') as mock_update:
        app.on_add_custom_click(None)
        assert ("CustomFolder", ["custom"]) in app.custom_folders
        assert any(isinstance(control, Text) and control.value == "CustomFolder: custom" for control in app.custom_list.controls)
        mock_update.assert_called()

def test_show_error_dialog(app):
    with mock.patch.object(app.page, 'update') as mock_update:
        app.show_error_dialog("Test error message")
        assert app.page.dialog.title.value == "Error"
        assert app.page.dialog.content.value == "Test error message"
        assert app.page.dialog.open is True
        mock_update.assert_called()

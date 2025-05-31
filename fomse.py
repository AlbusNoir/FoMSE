from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit, QMessageBox
from PyQt6 import uic
import sys
import os
import shutil
from pathlib import Path

# Fomse - Fields of Mistria Save Editor
# A simple save editor for the game Fields of Mistria, allowing users to unpack and pack save files using the VaultC executable.
# If needed: https://www.reddit.com/r/learnpython/comments/lkb8r3/pyqt5_and_pyinstaller_fail_to_build_exe/

# Currently only supporting Windows because Linux and MacOS don't natively run exe and I don't feel like fiddling with Mono or Wine compatibility
# Everything opens in either FOM_DIR or SAVES_DIR, users can figure out their own paths from there
LOCAL_APP_DATA = os.getenv('LOCALAPPDATA') # Defining global for local appdata since it's used a lot
FOM_DIR = os.path.join(LOCAL_APP_DATA, 'FieldsofMistria')  # Directory for Fields of Mistria
SAVES_DIR = os.path.join(FOM_DIR, 'saves')  # Directory for saves

class InfoWindow(QMainWindow):
    def __init__(self):
        super(InfoWindow, self).__init__()
        # Check for sys._MEIPASS
        bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        uic.loadUi(bundle_dir / 'info.ui', self)  # Load the UI file from the bundle directory

        self.setWindowTitle("Info")  # Set the window title
        self.show()  # Show the info window

class AboutWindow(QMainWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()

        # Check for sys._MEIPASS
        bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        uic.loadUi(bundle_dir / 'about.ui', self)  # Load the UI file from the bundle directory

        self.setWindowTitle("About")  # Set the window title
        self.show()  # Show the about window



class Fomse(QMainWindow):
    def __init__(self):
        super(Fomse, self).__init__()

        # Check for sys._MEIPASS
        bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        uic.loadUi(bundle_dir / 'fomse.ui', self)  # Load the UI file from the bundle directory

        self.setWindowTitle("Fields of Mistria Save Editor")  # Set the window title

        # Menu
        self.actionInfo.triggered.connect(self.open_info_window)  # Connect the Info action to the info window
        self.actionAbout.triggered.connect(self.open_about_window)  # Connect the About action to the about window
        

        # Widgets
        self.getFileBtn = self.findChild(QPushButton, 'getFileBtn')
        self.curFile = self.findChild(QLineEdit, 'curFile')
        self.selFileLbl = self.findChild(QLabel, 'selFileLbl')
        self.packBtn = self.findChild(QPushButton, 'packBtn')
        self.unpackBtn = self.findChild(QPushButton, 'unpackBtn')
        self.selDirLbl = self.findChild(QLabel, 'selDirLbl')
        self.curDir = self.findChild(QLineEdit, 'curDir')
        self.getDirBtn = self.findChild(QPushButton, 'getDirBtn')
        self.getExecBtn = self.findChild(QPushButton, 'getExecBtn')
        self.curExec = self.findChild(QLineEdit, 'curExec')
        self.selExecLbl = self.findChild(QLabel, 'selExecLbl')
        self.finBtn = self.findChild(QPushButton, 'finBtn')

        # getFileBtn
        self.getFileBtn.clicked.connect(self.get_savefile)

        # getDirBtn
        self.getDirBtn.clicked.connect(self.get_editdir)

        # getExecBtn
        self.getExecBtn.clicked.connect(self.get_exefile)

        # curFile
        self.curFile.setText("")  # Initialize the line edit with an empty string
        self.curFile.setReadOnly(True)  # Make the line edit read-only initially

        # curDir
        self.curDir.setText("")  # Initialize the line edit with an empty string
        self.curDir.setReadOnly(True)  # Make the line edit read-only initially

        # curExec
        self.curExec.setText("")  # Initialize the line edit with an empty string
        self.curExec.setReadOnly(True)  # Make the line edit read-only initially


        # packBtn
        self.packBtn.clicked.connect(self.pack_files)  # Connect the pack button to the pack function

        # unpackBtn
        self.unpackBtn.clicked.connect(self.unpack_files)  # Connect the unpack button to the unpack function
        
        self.show()  # Show the main window

    def requirements_check(self):
        # Check if the current file, directory, and executable are set
        if self.curFile.text() == "":
            # if the current file line edit is empty, show a message box
            msgBox = QMessageBox()
            msgBox.setWindowTitle("No File Selected")
            msgBox.setText("Please select a save file to unpack.")
            msgBox.exec()
            return
        if self.curDir.text() == "":
            # if the current directory line edit is empty, show a message box
            msgBox = QMessageBox()
            msgBox.setWindowTitle("No Directory Selected")
            msgBox.setText("Please select a directory to unpack to.")
            msgBox.exec()
            return
        if self.curExec.text() == "":
            # if the current executable line edit is empty, show a message box
            msgBox = QMessageBox()
            msgBox.setWindowTitle("No Executable Selected")
            msgBox.setText("Please select the VaultC executable to unpack the save file.")
            msgBox.exec()
            return
        # if all is fine, return
        return True  # All checks passed, return True

    def get_savefile(self):
        saves_dir = SAVES_DIR

        # Open a file dialog to select a save file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Save File", saves_dir, "Save Files (*.sav)")
        if file_name:
            self.curFile.setReadOnly(False)  # Make the line edit editable
            self.curFile.setText(f"{os.path.basename(file_name)}")
            self.curFile.setReadOnly(True)  # Make the line edit read-only again

    def get_editdir(self):
        fom_dir = FOM_DIR
        
        dir_name = QFileDialog.getExistingDirectory(self, "Select Directory to Unpack to", fom_dir, QFileDialog.Option.ShowDirsOnly)
        if dir_name:
            self.curDir.setReadOnly(False)  # Make the line edit editable
            self.curDir.setText(f"{os.path.basename(dir_name)}")
            self.curDir.setReadOnly(True)  # Make the line edit read-only again

            # set tooltip to show full path
            self.curDir.setToolTip(f"Full path: {dir_name}")

    def get_exefile(self):
        fom_dir = FOM_DIR
        
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Executable File", fom_dir, "Executable Files (*.exe)")
        if file_name:
            self.curExec.setReadOnly(False)
            self.curExec.setText(f"{os.path.basename(file_name)}")
            self.curExec.setReadOnly(True)  # Make the line edit read-only again
            # set tooltip to show full path
            self.curExec.setToolTip(f"Full path: {file_name}")


    def open_info_window(self):
        # Create and show the info window
        self.info_window = InfoWindow()
        self.info_window.show()

    def open_about_window(self):
        # Create and show the about window
        self.about_window = AboutWindow()
        self.about_window.show()

    def unpack_files(self): 
        if self.requirements_check():
        # if all checks pass, proceed with unpacking
            # set directory to saves location
            saves_dir = SAVES_DIR
            os.chdir(saves_dir) # This is just a sanity check

            text = self.curFile.text()  # Get the current file name from the line edit
            file = saves_dir + f"\\{text}"  # Construct the full file path
        
            # check for backup directory, create if it doesn't exist
            backup_dir = os.path.join(saves_dir, 'backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            else:
                src_file = file
                dest_file = os.path.join(backup_dir, os.path.basename(src_file))
                # check if the file already exists in the backup directory
                if os.path.exists(os.path.join(backup_dir, os.path.basename(file))):
                    # if it exists, ask the user if they want to overwrite it
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("File Already Exists. Overwrite?")
                    msgBox.setText(f"The file {os.path.basename(file)} already exists in the backup directory. Do you want to overwrite it?")
                    msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if msgBox.exec() == QMessageBox.StandardButton.Yes:
                        # if yes, delete the existing file
                        os.remove(os.path.join(backup_dir, os.path.basename(file)))
                        shutil.copy(src_file, dest_file)
                    else:
                        # if no, do not copy the file
                        return
                else:
                    # if it doesn't exist, copy the file to the backup directory
                    shutil.copy(src_file, dest_file)

            # after all the file shenanigans, do the actual unpacking
            # sanity check that we didn't move directories
            if not os.getcwd() == saves_dir:
                os.chdir(saves_dir)
        
            # now we can do the stuff
            unpack_dir_dirty = self.curDir.toolTip()  # Get the directory from the tooltip of the line edit
            unpack_dir_clean = unpack_dir_dirty.replace("Full path: ", "")
            exec_file_dirty = self.curExec.toolTip()  # Get the executable file from the tooltip of the line edit
            exec_file_clean = exec_file_dirty.replace("Full path: ", "")

            os.system(f'{exec_file_clean} unpack {file} {unpack_dir_clean}') # Run unpack command
        
            # Open the unpacked directory in Explorer
            os.chdir(unpack_dir_clean)
            os.system("explorer .")
    

    def pack_files(self):
        if self.requirements_check():
            # if all checks pass, proceed with packing
            # set directory to saves location
            saves_dir = SAVES_DIR
            os.chdir(saves_dir)
            text = self.curFile.text()
            file = saves_dir + f"\\{text}" # This will be the packed file

            # we shouldn't need to check anything else, should be fine to just pack from the existing params
            unpack_dir_dirty = self.curDir.toolTip()  # Get the directory from the tooltip of the line edit
            unpack_dir_clean = unpack_dir_dirty.replace("Full path: ", "")
            exec_file_dirty = self.curExec.toolTip()  # Get the executable file from the tooltip of the line edit
            exec_file_clean = exec_file_dirty.replace("Full path: ", "")

            os.system(f'{exec_file_clean} pack \"{unpack_dir_clean}\" \"{file}\"') # Run the pack command

        # Run cleanup
        self.clean_up()


    def clean_up(self):
        # tidy up the unpacked directory so we don't run into issues later
        if self.curDir.text() == "":
            # if the current directory line edit is empty, show a message box
            msgBox = QMessageBox()
            msgBox.setWindowTitle("No Directory Selected")
            msgBox.setText("Please select a directory to clean up.")
            msgBox.exec()
            return
        unpack_dir_dirty = self.curDir.toolTip()
        unpack_dir_clean = unpack_dir_dirty.replace("Full path: ", "")

        os.system(f'del /q \"{unpack_dir_clean}\\*\"')  # Delete all files in the unpacked directory



# Initialize the application
app = QApplication(sys.argv)
UIWindow = Fomse()  # Create an instance of the Fomse class
app.exec()  # Start the application event loop
sys.exit(app)  # Exit the application when the event loop ends
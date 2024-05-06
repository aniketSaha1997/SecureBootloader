import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
)

from flasher_layout import STM32UpdaterLayout

import serial  # For serial communication
import time  # For delay or time-based operations

# Main application class using QMainWindow
class STM32Updater(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initializing the imported layout
        self.layout = STM32UpdaterLayout()
        self.setCentralWidget(self.layout)  # Setting the central widget

        self.setWindowTitle("STM32 Updater")

        screen = QtWidgets.QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()  # Get screen geometry

        window_width = screen_rect.width() // 2  # Half the screen width
        window_height = screen_rect.height() // 2  # Half the screen height

        self.setGeometry(
            (screen_rect.width() - window_width) // 2,  # X position to center
            (screen_rect.height() - window_height) // 2,  # Y position to center
            window_width,  # Half the screen width
            window_height,  # Half the screen height
        )
        
        self.setMinimumSize(window_width, window_height)
        self.setMaximumSize(window_width, window_height)

        # Signal connections and logic
        self.layout.select_file_btn.clicked.connect(self.select_file)
        self.layout.update_btn.clicked.connect(self.start_upload)
        self.layout.cancel_btn.clicked.connect(self.cancel_upload)
        self.layout.full_chip_erase_btn.clicked.connect(self.full_chip_erase)
        self.layout.erase_sector_btn.clicked.connect(self.erase_selected_sector)
        self.layout.connect_button.clicked.connect(self.connect_or_disconnect)

        self.selected_file = None  # Variable initialization
        self.serial_port = None  # Serial port initialization
        self.uploading = False  # Initially, there is no ongoing upload
        

    def connect_or_disconnect(self):
        # Function to connect or disconnect the serial port
        if self.serial_port and self.serial_port.is_open:
            # Disconnect logic
            self.serial_port.close()
            self.layout.connect_button.setText("Connect")  # Change button text
            self.layout.com_port_selector.setEnabled(True)
            self.layout.disable_buttons()
            self.layout.disable_sector_dropdown()
            QMessageBox.information(self, "Disconnected", "Serial port has been disconnected.")
        else:
            # Connect logic
            self.init_serial_port()
            self.layout.connect_button.setText("Disconnect")  # Change button text
            self.layout.com_port_selector.setEnabled(False)
            self.layout.enable_buttons()
            self.layout.enable_sector_dropdown()
            QMessageBox.information(self, "Connected", "Serial port has been connected.")


    def select_file(self):
        # File selection logic
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Binary File", "", "Binary Files (*.bin)"
        )
        if file_name:
            self.selected_file = file_name
            self.layout.file_label.setText(file_name)
        else:
            self.selected_file = None


    def start_upload(self):
        if not self.uploading:
            self.uploading = True  # Set the flag to start the upload

            # Enable the "Cancel" button and start the upload
            self.layout.cancel_btn.setEnabled(True)
            self.upload_binary()  # Start the upload process

    def cancel_upload(self):
        # If cancel button is clicked, set uploading to False and reset styles
        self.uploading = False
        self.layout.cancel_btn.setEnabled(False)  # Disable the "Cancel" button
        self.layout.progress_bar.setValue(0)
        self.layout.progress_bar.setFormat("0%")
       # QtWidgets.QMessageBox.information(self, "Upload Canceled", "The upload was canceled.")


    def start_update(self):
        if not self.uploading:
            return  # If upload was canceled, do nothing

        if not self.serial_port or not self.serial_port.is_open:
            QtWidgets.QMessageBox.warning(self, "Not Connected", "Please connect to a serial port first.")
            return

        if not self.selected_file:
            QtWidgets.QMessageBox.warning(
                self,
                "No File Selected",
                "Please select a binary file before starting the update.",
            )
            return

        # Start the upload process
        self.upload_binary()


    def init_serial_port(self):
        # Check if the serial port is already initialized and open
        if self.serial_port and self.serial_port.is_open:
            return  # If already open, do nothing

        # Get the selected COM port from the ComboBox
        selected_port = self.layout.com_port_selector.currentText()

        # Initialize the serial port if it's not initialized
        if not self.serial_port:
            self.serial_port = serial.Serial(
                port=selected_port,
                baudrate=115200,
                timeout=1,
            )

        # Open the serial port if it's not already open
        if not self.serial_port.is_open:
            self.serial_port.open()


    def upload_binary(self):
        if not self.uploading:
            return  # If the upload flag is set to False, stop early

        # Check the serial port and selected file
        if not self.serial_port or not self.serial_port.is_open:
            QtWidgets.QMessageBox.warning(self, "Not Connected", "Please connect to a serial port first.")
            return

        if not self.selected_file:
            QtWidgets.QMessageBox.warning(
                self,
                "No File Selected",
                "Please select a binary file before starting the update.",
            )
            return

        with open(self.selected_file, "rb") as file:
            data = file.read()
            total_size = len(data)
            chunk_size = 4
            sent_size = 0

            try:
                while sent_size < total_size:
                    if not self.uploading:
                        self.layout.reset_upload_style() 
                        raise Exception("Upload canceled.")  # Stop the loop

                    # Write data to the serial port
                    chunk = data[sent_size : sent_size + chunk_size]
                    self.serial_port.write(chunk)
                    sent_size += chunk_size

                    # Update the progress bar
                    progress = (sent_size / total_size) * 100
                    self.layout.progress_bar.setValue(int(progress))
                    self.layout.progress_bar.setFormat(f"{int(progress)}%")

                    QtWidgets.QApplication.processEvents()  # Keep the GUI responsive

                QtWidgets.QMessageBox.information(self, "Update Complete", "The update was successful.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred during the update: {str(e)}")
            finally:
                # Reset the flag and the state of the "Cancel" button
                self.uploading = False
                self.layout.cancel_btn.setEnabled(False)  # Disable the "Cancel" button




    def full_chip_erase(self):
        try:
            self.init_serial_port()
            self.serial_port.write(b'FULL_CHIP_ERASE')
            QMessageBox.information(self, "Full Chip Erase", "Full chip erase initiated.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to erase chip: {str(e)}")

    def erase_selected_sector(self):
        try:
            self.init_serial_port()
            sector = self.layout.sector_dropdown.currentText().split()[-1]
            self.serial_port.write(f"ERASE_SECTOR {sector}".encode())
            QMessageBox.information(self, f"Erase Sector {sector}", f"Sector {sector} erase initiated.")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to erase sector: {str(e)}"
            )

    def closeEvent(self, event):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        super().closeEvent(event)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = STM32Updater()

    icon_path = os.path.join(os.path.dirname(__file__), "icons", "logo.png")
    if os.path.exists(icon_path):
        window.setWindowIcon(QtGui.QIcon(icon_path))
    else:
        print("Icon file not found at:", icon_path)  # Error message for debugging

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
)

from STM32FlasherLayout import STM32UpdaterLayout

import serial  # For serial communication


class STM32Updater(QMainWindow):
    """Main application class for the STM32 Updater GUI."""

    def __init__(self):
        super().__init__()

        # Initialize the imported layout
        self.layout = STM32UpdaterLayout()
        self.setCentralWidget(self.layout)  # Set the central widget for the window

        self.setWindowTitle("STM32 Updater")  # Set window title

        # Get screen geometry for centering the window
        screen = QtWidgets.QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        # Set window dimensions and center it
        window_width = screen_rect.width() // 2
        window_height = screen_rect.height() // 2
        self.setGeometry(
            (screen_rect.width() - window_width) // 2,
            (screen_rect.height() - window_height) // 2,
            window_width,
            window_height,
        )

        self.setMinimumSize(window_width, window_height)
        self.setMaximumSize(window_width, window_height)

        # Initialize default states
        self.selected_file = None  # No file selected initially
        self.serial_port = None  # Serial port is not initialized
        self.uploading = False  # No ongoing upload initially

        # Connect UI signals to their respective functions
        self.setup_signals()

    def setup_signals(self):
        """Connects UI signals to their respective functions."""
        self.layout.select_file_btn.clicked.connect(self.select_file)
        self.layout.update_btn.clicked.connect(self.start_upload)
        self.layout.cancel_btn.clicked.connect(self.cancel_upload)
        self.layout.full_chip_erase_btn.clicked.connect(self.full_chip_erase)
        self.layout.erase_sector_btn.clicked.connect(self.erase_selected_sector)
        self.layout.connect_button.clicked.connect(self.connect_or_disconnect)

    def connect_or_disconnect(self):
        """Connects to or disconnects from the serial port based on its current state."""
        if self.serial_port and self.serial_port.is_open:
            # Disconnect if the serial port is open
            self.serial_port.close()
            self.layout.connect_button.setText("Connect")  # Update button text
            self.layout.com_port_selector.setEnabled(True)  # Re-enable COM port selector
            self.layout.disable_buttons()  # Disable buttons
            self.layout.disable_sector_dropdown()  # Disable sector dropdown
            QMessageBox.information(self, "Disconnected", "The serial port has been disconnected.")
        else:
            # Attempt to connect if the serial port is not open
            connection_success = self.init_serial_port()
            
            if connection_success:
                self.layout.connect_button.setText("Disconnect")  # Update button text
                self.layout.com_port_selector.setEnabled(False)  # Disable COM port selector
                self.layout.enable_buttons()  # Enable other buttons
                self.layout.enable_sector_dropdown()  # Enable sector dropdown
                QMessageBox.information(self, "Connected", "Successfully connected to the COM port.")

    def select_file(self):
        """Allows the user to select a binary file for uploading."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Binary File", "", "Binary Files (*.bin)"
        )
        if file_name:
            self.selected_file = file_name
            self.layout.file_label.setText(file_name)
        else:
            self.selected_file = None

    def start_upload(self):
        """Starts the binary upload process."""
        if self.uploading:
            return  # If already uploading, do nothing
        
        self.uploading = True  # Mark the beginning of the upload process
        self.layout.cancel_btn.setEnabled(True)  # Enable the "Cancel" button
        self.upload_binary()  # Begin the binary upload

    def cancel_upload(self):
        """Cancels the ongoing binary upload."""
        self.uploading = False  # Stop the upload process
        self.layout.cancel_btn.setEnabled(False)  # Disable the "Cancel" button
        self.layout.reset_upload_style()  # Reset upload-related styles

    def init_serial_port(self):
        """Initializes the serial port based on the selected COM port."""
        selected_port = self.layout.com_port_selector.currentText()

        if not selected_port:
            # If no COM port is selected, display a warning and exit early
            QtWidgets.QMessageBox.warning(self, "No COM Port Selected", "Please select a COM port before connecting.")
            return False  # Return failure status

        try:
            # Initialize the serial port if not already done
            if not self.serial_port:
                self.serial_port = serial.Serial(
                    port=selected_port,
                    baudrate=115200,  # Example baud rate
                    timeout=1,  # Example timeout
                )

            if not self.serial_port.is_open:
                self.serial_port.open()  # Open the serial port

            return True  # Return success status

        except serial.SerialException as se:
            QtWidgets.QMessageBox.critical(self, "Serial Port Error", f"Could not open the COM port: {str(se)}")
            return False  # Return failure status

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            return False  # Return failure status

    def upload_binary(self):
        """Handles the binary upload to the serial port."""
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

        with open(self.selected_file, "rb") as file:
            data = file.read()
            total_size = len(data)
            chunk_size = 4  # Define a chunk size for data transfer
            sent_size = 0

            try:
                while sent_size < total_size:
                    if not self.uploading:
                        # If upload is canceled, reset the style and stop
                        self.layout.reset_upload_style()
                        raise Exception("Upload canceled.")

                    # Write the current chunk to the serial port
                    chunk = data[sent_size:sent_size + chunk_size]
                    self.serial_port.write(chunk)
                    sent_size += chunk_size

                    # Update the progress bar
                    progress = (sent_size / total_size) * 100
                    self.layout.progress_bar.setValue(int(progress))
                    self.layout.progress_bar.setFormat(f"{int(progress)}%")

                    # Keep the GUI responsive
                    QtWidgets.QApplication.processEvents()

                QtWidgets.QMessageBox.information(self, "Update Complete", "The update was successful.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred during the update: {str(e)}")
            finally:
                # Reset the uploading flag and disable the "Cancel" button
                self.uploading = False
                self.layout.cancel_btn.setEnabled(False)  # Disable "Cancel"

    def full_chip_erase(self):
        """Erases the entire chip."""
        try:
            self.init_serial_port()  # Ensure the serial port is connected
            self.serial_port.write(b'FULL_CHIP_ERASE')  # Send erase command
            QtWidgets.QMessageBox.information(self, "Full Chip Erase", "Full chip erase initiated.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to erase the chip: {str(e)}")

    def erase_selected_sector(self):
        """Erases the selected sector on the chip."""
        try:
            self.init_serial_port()  # Ensure the serial port is connected
            sector = self.layout.sector_dropdown.currentText().split()[-1]  # Get the selected sector
            self.serial_port.write(f"ERASE_SECTOR {sector}".encode())  # Send erase command
            QtWidgets.QMessageBox.information(
                self, f"Erase Sector {sector}", f"Sector {sector} erase initiated."
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Failed to erase sector: {str(e)}"
            )

    def closeEvent(self, event):
        """Closes the serial port when the window is closed."""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        super().closeEvent(event)


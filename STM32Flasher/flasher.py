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
        self.layout.update_btn.clicked.connect(self.start_update)
        self.layout.full_chip_erase_btn.clicked.connect(self.full_chip_erase)
        self.layout.erase_sector_btn.clicked.connect(self.erase_selected_sector)

        self.selected_file = None  # Variable initialization
        self.serial_port = None  # Serial port initialization

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

    def start_update(self):
        if not self.selected_file:
            QMessageBox.warning(
                self,
                "No File Selected",
                "Please select a binary file before starting the update.",
            )
            return

        # Initialize serial port
        self.init_serial_port()

        # Start the upload process
        self.upload_binary()

    def init_serial_port(self):
        if not self.serial_port:
            self.serial_port = serial.Serial(
                port="COM1", baudrate=115200, timeout=1
            )
        if not self.serial_port.is_open:
            self.serial_port.open()

    def upload_binary(self):
        if self.selected_file is None:
            QMessageBox.warning(
                self,
                "No File Selected",
                "Please select a file to upload.",
            )
            return

        with open(self.selected_file, "rb") as file:
            data = file.read()
            total_size = len(data)
            chunk_size = 4
            sent_size = 0

            while sent_size < total_size:
                chunk = data[sent_size : sent_size + chunk_size]
                self.serial_port.write(chunk)
                sent_size += chunk_size

                progress = (sent_size / total_size) * 100
                self.layout.progress_bar.setValue(int(progress))

                time.sleep(0.01)

        QMessageBox.information(self, "Update Complete", "The update was successful.")

    def full_chip_erase(self):
        try:
            self.init_serial_port()
            self.serial_port.write(b'CHIP_ERASE')
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

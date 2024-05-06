from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QComboBox,
    QProgressBar,
    QWidget,
    QSpacerItem,
    QSizePolicy,
)
import serial.tools.list_ports
from cssStyles import CSS_BUTTON_DEFAULT
from cssStyles import CSS_COMBO_BOX_DEFAULT

class STM32UpdaterLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Get the available screen geometry
        screen = QtWidgets.QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()  # Get screen geometry
        
        # Set the window size to half the screen width and height
        window_width = screen_rect.width() // 2  # Half the screen width
        window_height = screen_rect.height() // 2  # Half the screen height

        # Center the window on the screen
        self.setGeometry(
            (screen_rect.width() - window_width) // 2,  # X position to center
            (screen_rect.height() - window_height) // 2,  # Y position to center
            window_width,  # Half the screen width
            window_height  # Half the screen height
        )

        self.setMinimumSize(window_width, window_height)  # Fixed minimum size
        self.setMaximumSize(window_width, window_height)  # Fixed maximum size
        
        # Define widget positions and sizes relative to the window size
        spacingWidth  = 10  # Standard spacing between widgets
        spacingHeight = 30

        # Port label and ComboBox
        port_label_font = QFont("Arial", 12)  # Font settings
        port_label = QLabel("Port", self)
        port_label.setFont(port_label_font)
        port_label.setGeometry(spacingWidth, spacingHeight, 60, 30)

        self.com_port_selector = QComboBox(self)
        self.com_port_selector.setGeometry(80, spacingHeight, 200, 30)  # Adjusted to fit within the window
        self.populate_com_ports()

        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.setGeometry(290, spacingHeight, 120, 30)  # Fixed position and width
        self.disconnect_button.setStyleSheet(CSS_BUTTON_DEFAULT)  # Apply the style

        # File selection button and label
        select_file_label_font = QFont("Arial", 12)  # Font settings
        select_file_label = QLabel("Binary", self)
        select_file_label.setFont(select_file_label_font)
        select_file_label.setGeometry(spacingWidth, spacingHeight + 50, 60, 30)

        self.select_file_btn = QPushButton("Select File", self)
        self.select_file_btn.setGeometry(80, spacingHeight + 50, 120, 30)
        self.select_file_btn.setStyleSheet(CSS_BUTTON_DEFAULT)  # Apply the style

        self.file_label = QLabel("No file selected", self)
        self.file_label.setGeometry(220, spacingHeight + 50, window_width - 150, 30)  # Adjusted to fit

        # Full chip erase button
        self.full_chip_erase_btn = QPushButton("Full Chip Erase", self)
        self.full_chip_erase_btn.setGeometry(spacingWidth + 200, spacingHeight + 250, 160, 30)
        self.full_chip_erase_btn.setStyleSheet(CSS_BUTTON_DEFAULT)  # Apply the style

        # Erase sector button and dropdown
        self.erase_sector_btn = QPushButton("Erase Sector", self)
        self.erase_sector_btn.setGeometry(spacingWidth + 390, spacingHeight + 250, 160, 30)
        self.erase_sector_btn.setStyleSheet(CSS_BUTTON_DEFAULT)  # Apply the style

        self.sector_dropdown = QComboBox(self)
        self.sector_dropdown.setGeometry(spacingWidth + 580, spacingHeight + 250, 140, 30)
        self.sector_dropdown.setStyleSheet(CSS_COMBO_BOX_DEFAULT)  # Apply the style
        for i in range(9):
            self.sector_dropdown.addItem(f"Sector {i}")

        # Progress bar and "Start Update" button
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(spacingWidth, window_height - 50, window_width - 150, 30)

        # Set initial progress value and format
        self.progress_bar.setValue(0)  # Start at 0%
        self.progress_bar.setFormat("0%")  # Display 0% inside the bar

        # Ensure the progress bar text appears within the bar
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(True)

        self.update_btn = QPushButton("Start Update", self)
        self.update_btn.setGeometry(window_width - 130, window_height - 50, 120, 30)
        self.update_btn.setStyleSheet(CSS_BUTTON_DEFAULT)  # Apply the style
        

    def populate_com_ports(self):
        # Clear the ComboBox and add available COM ports
        self.com_port_selector.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_selector.addItem(port.device)

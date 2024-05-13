from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QComboBox,
    QProgressBar,
    QWidget,
)
import serial.tools.list_ports
from cssStyles import CSS_BUTTON_DEFAULT, CSS_LABEL_GREY, CSS_COMBO_BOX_DEFAULT


class STM32UpdaterLayout(QtWidgets.QWidget):
    """Defines the layout and UI components for the STM32 updater application."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Get the screen dimensions for centering the window
        screen = QtWidgets.QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        # Set window size and center it on the screen
        window_width = screen_rect.width() // 2  # Half the screen width
        window_height = screen_rect.height() // 2  # Half the screen height
        self.setGeometry(
            (screen_rect.width() - window_width) // 2,
            (screen_rect.height() - window_height) // 2,
            window_width,
            window_height,
        )

        # Set minimum and maximum window size
        self.setMinimumSize(window_width, window_height)
        self.setMaximumSize(window_width, window_height)

        # Initialize UI components and set positions
        self.initialize_ui(window_width, window_height)

        # Set up a timer to refresh COM ports every 2 seconds
        self.com_port_refresh_timer = QtCore.QTimer(self)
        self.com_port_refresh_timer.timeout.connect(self.refresh_com_ports)
        self.com_port_refresh_timer.start(2000)  # Refresh every 2 seconds

    def initialize_ui(self, window_width, window_height):
        """Initializes the user interface components and their positions."""
        spacing_width = 10  # Standard spacing between widgets
        spacing_height = 30

        # Create label and ComboBox for COM ports
        port_label = QLabel("Port", self)
        port_label.setFont(QFont("Arial", 12))
        port_label.setGeometry(spacing_width, spacing_height, 60, 30)

        self.com_port_selector = QComboBox(self)
        self.com_port_selector.setGeometry(80, spacing_height, 200, 30)  # Adjusted to fit
        self.populate_com_ports()  # Populate available COM ports

        # Connect button
        self.connect_button = QPushButton("Connect", self)
        self.connect_button.setGeometry(290, spacing_height, 120, 30)  # Fixed position and width
        self.connect_button.setStyleSheet(CSS_BUTTON_DEFAULT)

        # File selection components
        self.select_file_btn = QPushButton("Select File", self)
        self.select_file_btn.setGeometry(80, spacing_height + 50, 120, 30)
        self.select_file_btn.setStyleSheet(CSS_BUTTON_DEFAULT)

        self.file_label = QLabel("No file selected", self)
        self.file_label.setGeometry(220, spacing_height + 50, window_width - 150, 30)  # Adjusted to fit

        # Full chip erase button
        self.full_chip_erase_btn = QPushButton("Full Chip Erase", self)
        self.full_chip_erase_btn.setGeometry(spacing_width + 220, spacing_height + 250, 160, 30)
        self.full_chip_erase_btn.setStyleSheet(CSS_BUTTON_DEFAULT)

        # Erase sector button and dropdown
        self.erase_sector_btn = QPushButton("Erase Sector", self)
        self.erase_sector_btn.setGeometry(spacing_width + 390, spacing_height + 250, 160, 30)
        self.erase_sector_btn.setStyleSheet(CSS_BUTTON_DEFAULT)

        self.sector_dropdown = QComboBox(self)
        self.sector_dropdown.setGeometry(spacing_width + 560, spacing_height + 250, 140, 30)  # Adjusted
        self.sector_dropdown.setStyleSheet(CSS_COMBO_BOX_DEFAULT)  # Apply style
        for i in range (9):
            self.sector_dropdown.addItem(f"Sector {i}")

        # Progress bar and control buttons
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(spacing_width + 50, window_height - 100, window_width - 120, 30)
        self.progress_bar.setValue(0)  # Initial value
        self.progress_bar.setFormat("0%")  # Display 0% initially
        self.progress_bar.setAlignment(Qt.AlignCenter)

        self.update_btn = QPushButton("Start Update", self)
        self.update_btn.setGeometry(spacing_width + 334, window_height - 50, 120, 30)  # Fixed position and size
        self.update_btn.setStyleSheet(CSS_BUTTON_DEFAULT)

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(spacing_width + 474, window_height - 50, 120, 30)  # Fixed position
        self.cancel_btn.setStyleSheet(CSS_BUTTON_DEFAULT)

        # Initial button state
        self.update_btn.setEnabled(False)  # Disable initially
        self.full_chip_erase_btn.setEnabled(False)
        self.erase_sector_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)  # Start with all major operations disabled
        self.sector_dropdown.setEnabled(False)  # Start with sector dropdown disabled
        self.sector_dropdown.setStyleSheet(CSS_LABEL_GREY)  # Grey to indicate disabled state

    def enable_buttons(self):
        """Enables the primary operation buttons."""
        self.update_btn.setEnabled(True)
        self.full_chip_erase_btn.setEnabled(True)
        self.erase_sector_btn.setEnabled(True)

    def disable_buttons(self):
        """Disables the primary operation buttons."""
        self.update_btn.setEnabled(False)
        self.full_chip_erase_btn.setEnabled(False)
        self.erase_sector_btn.setEnabled(False)

    def enable_sector_dropdown(self):
        """Enables the sector dropdown with default styling."""
        self.sector_dropdown.setEnabled(True)
        self.sector_dropdown.setStyleSheet(CSS_COMBO_BOX_DEFAULT)

    def disable_sector_dropdown(self):
        """Disables the sector dropdown with grey styling."""
        self.sector_dropdown.setEnabled(False)
        self.sector_dropdown.setStyleSheet(CSS_LABEL_GREY)

    def populate_com_ports(self):
        """Populate the ComboBox with available COM ports."""
        self.com_port_selector.clear()  # Clear existing items
        ports = serial.tools.list_ports.comports()  # Get a list of available COM ports
        for port in ports:
            self.com_port_selector.addItem(port.device)

    def refresh_com_ports(self):
        """Refreshes the ComboBox with updated COM ports."""
        current_selection = self.com_port_selector.currentText()  # Remember the current selection
        
        # Refresh the COM ports
        self.populate_com_ports()

        # Restore the current selection if it still exists
        if current_selection in [self.com_port_selector.itemText(i) for i in range(self.com_port_selector.count())]:
            self.com_port_selector.setCurrentText(current_selection)

    def reset_upload_style(self):
        """Resets the buttons after cancel, for next  upload operation."""
        self.update_btn.setStyleSheet(CSS_BUTTON_DEFAULT)  # Reset to default style
        self.progress_bar.setValue(0)  # Reset progress bar to 0
        self.progress_bar.setFormat("0%")  # Display 0%
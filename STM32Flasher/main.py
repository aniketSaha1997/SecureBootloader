import sys
from PyQt5 import QtWidgets
from flasher import STM32Updater  # Import the main class from flasher

def main():
    """Main entry point for the STM32 updater application."""
    app = QtWidgets.QApplication(sys.argv)  # Initialize the Qt application
    window = STM32Updater()  # Create the main application window
    window.show()  # Show the main window
    sys.exit(app.exec_())  # Start the event loop


if __name__ == "__main__":
    main()  # Run the main function if this script is executed

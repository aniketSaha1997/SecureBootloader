# SecureBootloader
# STM32 Flasher GUI

The STM32 Flasher GUI is a graphical user interface (GUI) application designed to interface with STM32 microcontrollers via USB or serial ports. This application allows users to connect to STM32 devices, select binary files, and flash them to the microcontroller. It provides additional features like full chip erase, sector-specific erase, and progress tracking during updates.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)

## Features
- Connect to STM32 devices via USB or serial ports.
- Select and upload binary files to the microcontroller.
- Full chip erase and sector-specific erase functionality.
- Progress tracking with a progress bar and percentage display.
- Graphical user interface for ease of use.

## Installation
To install and run the STM32 Flasher GUI, you'll need Python and PyQt5. Follow these steps:

1. Clone the repository:
   ```bash
    git clone https://github.com/your-username/stm32-flasher-gui.git
   
2. Enter the dedicated folder:
   ```bash
    cd STM32Flasher

3. Install the required dependencies:
   ```bash
    pip install -r requirements.txt

## Usage
1. To run the STM32 Flasher GUI, execute the following command from your terminal:
   ```bash
    python main.py

This command starts the GUI application. Here's a basic guide to using the application:

- **Connect to STM32:** Select a COM port from the dropdown list and click the "Connect" button.
- **Select a Binary File:** Click the "Select File" button to choose the binary file you want to upload to the STM32 device.
- **Start the Upload:** Click "Start Update" to begin the upload process. A progress bar indicates the upload status.
- **Cancel (if needed):** Click the "Cancel" button to stop the upload process.
- **Additional Operations:** Use the "Full Chip Erase" button to erase the entire chip or the "Erase Sector" button to erase a specific sector.


## Development
To develop and test the STM32 Flasher GUI, ensure you have the following:

- **Development Environment:** Python and a suitable IDE or text editor.
- **PyInstaller: Use PyInstaller:** to create standalone executables.


**Creating an Executable with PyInstaller:**
1. To create a standalone executable (EXE) from your Python application, you can use PyInstaller. The following command generates a single EXE file from main.py:
   ```bash
    pyinstaller --onefile --windowed --name STM32Flasher main.py
- --onefile: Creates a single executable.
- --windowed: Ensures it runs as a GUI application without a console window.
- --name STM32Flasher: Sets the name of the resulting EXE.







#!/usr/bin/env python3
# encode: utf8

"""
@file

@version    $Revision:$
@change     $Change:$
@date       $Date:$
@authors    $Author:$

@brief      Contains default CSS styles for PyQt widgets to maintain consistent styling across the application.
"""

CSS_BUTTON_DEFAULT = """
    QPushButton:enabled {
        background-color: #42A5F5;
        border-radius: 10px;
        border: 1px solid #1976D2;
        color: #FFFFFF;
        font-size: 16px;
        padding: 4px 4px;
        text-align: center;
        text-decoration: none;
    }

    QPushButton:hover {
        background-color: #64B5F6;
        border-color: #0D47A1;
    }

    QPushButton:disabled {
        background-color: #E0E0E0;
        border-radius: 10px;
        border: 1px solid #BDBDBD;
        color: #9E9E9E;
        font-size: 16px;
        padding: 4px 4px;
        text-align: center;
        text-decoration: none;
    }
"""

CSS_BUTTON_RED = """
    QPushButton {
        background-color: darkred;
        border-radius: 10px;  # Rounded corners
        border: 1px solid darkred;  # Dark red border
        color: white;  # White text
        font-size: 16px;  # Font size
        padding: 4px 4px;  # Padding
        text-align: center;  # Text alignment
        text-decoration: none;  # No text decoration
    }
"""


CSS_LED_DEFAULT = "border-radius: 15px; background-color: red;"

CSS_LABEL_BLACK = "color: black;"

CSS_LABEL_GREY = "color: grey;"

CSS_COMBO_BOX_DEFAULT = """
    QComboBox {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7cb3ff, stop:1 #E1F5FE);
        border-top-left-radius: 16px;
        border-bottom-left-radius: 16px;
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;
        border: 1px solid #1976D2;
        color: #000000;
        font-size: 16px;
        padding: 1px 1px;
        text-align: center;
        text-decoration: none;
    }

    QComboBox:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7cb3ff, stop:1 #7cb3ff);
        border-color: #0D47A1;
    }
"""

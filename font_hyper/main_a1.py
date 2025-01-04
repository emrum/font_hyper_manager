# main_a1.py

import sys
import tkinter as tk
from .gui_main_window import FontHyperGUI
import logging

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create console handler and set level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

# Create file handler and set level
fh = logging.FileHandler('font_hyper.log')
fh.setLevel(logging.INFO)

# Create formatter and add to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


def main():
    """Entry point for the Font Hyper application."""
    try:
        root = tk.Tk()
        app = FontHyperGUI(root)
        root.mainloop()
    except Exception as e:
        logger.exception("Exception in main function")
        sys.exit(1)


if __name__ == "__main__":
    main()

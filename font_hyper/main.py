#!/usr/bin/env python3

import sys
sys.path.append("..")
from font_hyper.gui_main_window import FontHyperGUI

import tkinter as tk
import logging
import traceback



def setup_logging():
    """Configure application-wide logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler('font_hyper.log')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

def main():
    """Main entry point for the Font Hyper application."""
    # Set up logging
    logger = setup_logging()
    logger.info("Starting Font Hyper application")

    try:
        # Create root window
        root = tk.Tk()
        root.title("Font Hyper")

        # Set minimum window size
        root.minsize(1200, 700)
        # root.geometry("1200,700") # error: bad specifier

        # Initialize main application
        app = FontHyperGUI(root)
        
        # Start main event loop
        logger.info("Entering main event loop")
        root.mainloop()

    except Exception as e:
        # Log the full exception traceback
        logger.critical(f"Fatal error in main application: {str(e)}")
        logger.critical(traceback.format_exc())
        
        # Show error to user if GUI is available
        if 'root' in locals() and isinstance(root, tk.Tk):
            try:
                from tkinter import messagebox
                messagebox.showerror("Fatal Error",
                    "A fatal error has occurred. Check the log file for details.\n\n" +
                    f"Error: {str(e)}")
            except:
                pass  # If messagebox fails, at least we have the log
        
        sys.exit(1)

    logger.info("Application terminated normally")

if __name__ == "__main__":
    main()
    

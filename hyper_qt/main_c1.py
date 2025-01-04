


from PySide6.QtWidgets import QApplication, QMainWindow
from generated_main_window  import Ui_MainWindow  # Import the generated UI class

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Set up the UI

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()


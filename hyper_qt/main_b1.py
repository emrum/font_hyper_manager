from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QCoreApplication
import sys

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = "qt6_main_window.ui"
        self.ui = loader.load(ui_file, self)

        # Create QSplitter
#        self.splitter = QSplitter(Qt.Horizontal, self.ui.centralwidget)

        # Find the widgets created in Designer
#        self.frame1 = self.ui.findChild(QWidget, "frame1")
#        self.frame2 = self.ui.findChild(QWidget, "frame2")

        # Add the frames to the splitter
#        self.splitter.addWidget(self.frame1)
#        self.splitter.addWidget(self.frame2)

        # Set the splitter as the central widget
#        self.ui.verticalLayout.addWidget(self.splitter)

        self.setCentralWidget(self.ui)

if __name__ == "__main__":
    #Qt.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())


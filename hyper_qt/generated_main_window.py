# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt6_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGraphicsView,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSlider, QStatusBar, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1075, 761)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionTell_me_how = QAction(MainWindow)
        self.actionTell_me_how.setObjectName(u"actionTell_me_how")
        self.actionTips = QAction(MainWindow)
        self.actionTips.setObjectName(u"actionTips")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.frame_TopRow = QFrame(self.centralwidget)
        self.frame_TopRow.setObjectName(u"frame_TopRow")
        self.frame_TopRow.setMinimumSize(QSize(0, 50))
        self.horizontalLayout_12 = QHBoxLayout(self.frame_TopRow)
        self.horizontalLayout_12.setSpacing(2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 2, 2, 2)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.groupBox_9 = QGroupBox(self.frame_TopRow)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(0, 50))
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_11.setSpacing(1)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(1, 1, 1, 1)
        self.listWidget_SysPaths = QListWidget(self.groupBox_9)
        self.listWidget_SysPaths.setObjectName(u"listWidget_SysPaths")
        self.listWidget_SysPaths.setMinimumSize(QSize(0, 24))
        self.listWidget_SysPaths.setMaximumSize(QSize(16777215, 90))

        self.verticalLayout_11.addWidget(self.listWidget_SysPaths)


        self.horizontalLayout_11.addWidget(self.groupBox_9)

        self.groupBox_8 = QGroupBox(self.frame_TopRow)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_12.setSpacing(1)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(1, 1, 1, 1)
        self.listWidget_UserPaths = QListWidget(self.groupBox_8)
        self.listWidget_UserPaths.setObjectName(u"listWidget_UserPaths")
        self.listWidget_UserPaths.setMinimumSize(QSize(0, 24))
        self.listWidget_UserPaths.setMaximumSize(QSize(16777215, 90))

        self.verticalLayout_12.addWidget(self.listWidget_UserPaths)


        self.horizontalLayout_11.addWidget(self.groupBox_8)

        self.groupBox = QGroupBox(self.frame_TopRow)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_13.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_13.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_13.addWidget(self.pushButton_3)


        self.horizontalLayout_11.addWidget(self.groupBox)


        self.horizontalLayout_12.addLayout(self.horizontalLayout_11)


        self.verticalLayout.addWidget(self.frame_TopRow)

        self.frame_SecondRow = QFrame(self.centralwidget)
        self.frame_SecondRow.setObjectName(u"frame_SecondRow")
        self.frame_SecondRow.setMinimumSize(QSize(0, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.frame_SecondRow)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_RenderFrame = QGroupBox(self.frame_SecondRow)
        self.groupBox_RenderFrame.setObjectName(u"groupBox_RenderFrame")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_RenderFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.groupBox_RenderOptions = QGroupBox(self.groupBox_RenderFrame)
        self.groupBox_RenderOptions.setObjectName(u"groupBox_RenderOptions")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_RenderOptions)
        self.verticalLayout_10.setSpacing(1)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_8 = QFrame(self.groupBox_RenderOptions)
        self.frame_8.setObjectName(u"frame_8")
        self.horizontalLayout_7 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.frame_8)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.checkBox = QCheckBox(self.frame_8)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_6.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.frame_8)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_6.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.frame_8)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.horizontalLayout_6.addWidget(self.checkBox_3)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)


        self.verticalLayout_9.addWidget(self.frame_8)

        self.lineEdit_RenderText = QLineEdit(self.groupBox_RenderOptions)
        self.lineEdit_RenderText.setObjectName(u"lineEdit_RenderText")

        self.verticalLayout_9.addWidget(self.lineEdit_RenderText)

        self.frame = QFrame(self.groupBox_RenderOptions)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 32))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame)
        self.horizontalLayout_10.setSpacing(1)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(1, 1, 1, 1)
        self.pushButton_SelectColor = QPushButton(self.frame)
        self.pushButton_SelectColor.setObjectName(u"pushButton_SelectColor")

        self.horizontalLayout_10.addWidget(self.pushButton_SelectColor)

        self.pushButton_ShowPaths = QPushButton(self.frame)
        self.pushButton_ShowPaths.setObjectName(u"pushButton_ShowPaths")

        self.horizontalLayout_10.addWidget(self.pushButton_ShowPaths)


        self.verticalLayout_9.addWidget(self.frame)

        self.label_CurrentFont = QLabel(self.groupBox_RenderOptions)
        self.label_CurrentFont.setObjectName(u"label_CurrentFont")
        self.label_CurrentFont.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_CurrentFont.setFont(font)

        self.verticalLayout_9.addWidget(self.label_CurrentFont)


        self.verticalLayout_10.addLayout(self.verticalLayout_9)


        self.verticalLayout_4.addWidget(self.groupBox_RenderOptions)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.graphicsView_Canvas = QGraphicsView(self.groupBox_RenderFrame)
        self.graphicsView_Canvas.setObjectName(u"graphicsView_Canvas")
        self.graphicsView_Canvas.setMinimumSize(QSize(0, 80))

        self.verticalLayout_3.addWidget(self.graphicsView_Canvas)

        self.horizontalSlider_FontSize = QSlider(self.groupBox_RenderFrame)
        self.horizontalSlider_FontSize.setObjectName(u"horizontalSlider_FontSize")
        self.horizontalSlider_FontSize.setMinimum(6)
        self.horizontalSlider_FontSize.setMaximum(92)
        self.horizontalSlider_FontSize.setValue(36)
        self.horizontalSlider_FontSize.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout_3.addWidget(self.horizontalSlider_FontSize)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addWidget(self.groupBox_RenderFrame)

        self.groupBox_CategoriesFrame = QGroupBox(self.frame_SecondRow)
        self.groupBox_CategoriesFrame.setObjectName(u"groupBox_CategoriesFrame")
        self.groupBox_CategoriesFrame.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_CategoriesFrame)
        self.verticalLayout_6.setSpacing(1)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.treeWidget_Categories = QTreeWidget(self.groupBox_CategoriesFrame)
        self.treeWidget_Categories.setObjectName(u"treeWidget_Categories")
        self.treeWidget_Categories.setMinimumSize(QSize(0, 80))

        self.verticalLayout_5.addWidget(self.treeWidget_Categories)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)


        self.horizontalLayout.addWidget(self.groupBox_CategoriesFrame)

        self.groupBox_CategoryActionsFrame = QGroupBox(self.frame_SecondRow)
        self.groupBox_CategoryActionsFrame.setObjectName(u"groupBox_CategoryActionsFrame")
        self.groupBox_CategoryActionsFrame.setMaximumSize(QSize(140, 16777215))
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_CategoryActionsFrame)
        self.verticalLayout_8.setSpacing(1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(1, 1, 1, 1)
        self.label_CategoryName = QLabel(self.groupBox_CategoryActionsFrame)
        self.label_CategoryName.setObjectName(u"label_CategoryName")

        self.verticalLayout_8.addWidget(self.label_CategoryName)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lineEdit_CategoryName = QLineEdit(self.groupBox_CategoryActionsFrame)
        self.lineEdit_CategoryName.setObjectName(u"lineEdit_CategoryName")

        self.verticalLayout_7.addWidget(self.lineEdit_CategoryName)

        self.pushButton_NewCategory = QPushButton(self.groupBox_CategoryActionsFrame)
        self.pushButton_NewCategory.setObjectName(u"pushButton_NewCategory")

        self.verticalLayout_7.addWidget(self.pushButton_NewCategory)

        self.pushButton_DeleteCategory = QPushButton(self.groupBox_CategoryActionsFrame)
        self.pushButton_DeleteCategory.setObjectName(u"pushButton_DeleteCategory")

        self.verticalLayout_7.addWidget(self.pushButton_DeleteCategory)

        self.pushButton_InsertFont = QPushButton(self.groupBox_CategoryActionsFrame)
        self.pushButton_InsertFont.setObjectName(u"pushButton_InsertFont")
        self.pushButton_InsertFont.setStyleSheet(u"background-color: rgb(255, 237, 196);")

        self.verticalLayout_7.addWidget(self.pushButton_InsertFont)

        self.pushButton_RemoveFont = QPushButton(self.groupBox_CategoryActionsFrame)
        self.pushButton_RemoveFont.setObjectName(u"pushButton_RemoveFont")
        self.pushButton_RemoveFont.setStyleSheet(u"background-color: rgb(255, 237, 196);")

        self.verticalLayout_7.addWidget(self.pushButton_RemoveFont)

        self.line = QFrame(self.groupBox_CategoryActionsFrame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.line_2 = QFrame(self.groupBox_CategoryActionsFrame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.pushButton_InstallCategory = QPushButton(self.groupBox_CategoryActionsFrame)
        self.pushButton_InstallCategory.setObjectName(u"pushButton_InstallCategory")
        self.pushButton_InstallCategory.setStyleSheet(u"background-color: rgb(255, 242, 255);\n"
"")

        self.verticalLayout_7.addWidget(self.pushButton_InstallCategory)

        self.pushButton_UninstallCategory = QPushButton(self.groupBox_CategoryActionsFrame)
        self.pushButton_UninstallCategory.setObjectName(u"pushButton_UninstallCategory")
        self.pushButton_UninstallCategory.setStyleSheet(u"background-color: rgb(255, 242, 255);")

        self.verticalLayout_7.addWidget(self.pushButton_UninstallCategory)

        self.pushButton_UpdateSysCache = QPushButton(self.groupBox_CategoryActionsFrame)
        self.pushButton_UpdateSysCache.setObjectName(u"pushButton_UpdateSysCache")

        self.verticalLayout_7.addWidget(self.pushButton_UpdateSysCache)

        self.frame_4 = QFrame(self.groupBox_CategoryActionsFrame)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_7.addWidget(self.frame_4)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)


        self.horizontalLayout.addWidget(self.groupBox_CategoryActionsFrame)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame_SecondRow)

        self.frame_ThirdRow = QFrame(self.centralwidget)
        self.frame_ThirdRow.setObjectName(u"frame_ThirdRow")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_ThirdRow.sizePolicy().hasHeightForWidth())
        self.frame_ThirdRow.setSizePolicy(sizePolicy2)
        self.frame_ThirdRow.setMinimumSize(QSize(0, 120))
        self.horizontalLayout_4 = QHBoxLayout(self.frame_ThirdRow)
        self.horizontalLayout_4.setSpacing(1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(4, 1, 1, 1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame_2 = QFrame(self.frame_ThirdRow)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_2)
        self.verticalLayout_14.setSpacing(4)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.lineEdit_SearchText = QLineEdit(self.frame_3)
        self.lineEdit_SearchText.setObjectName(u"lineEdit_SearchText")

        self.horizontalLayout_5.addWidget(self.lineEdit_SearchText)

        self.pushButton_ClearSearchText = QPushButton(self.frame_3)
        self.pushButton_ClearSearchText.setObjectName(u"pushButton_ClearSearchText")

        self.horizontalLayout_5.addWidget(self.pushButton_ClearSearchText)

        self.pushButton_HideSysPaths = QPushButton(self.frame_3)
        self.pushButton_HideSysPaths.setObjectName(u"pushButton_HideSysPaths")

        self.horizontalLayout_5.addWidget(self.pushButton_HideSysPaths)

        self.pushButton_HideUserPaths = QPushButton(self.frame_3)
        self.pushButton_HideUserPaths.setObjectName(u"pushButton_HideUserPaths")

        self.horizontalLayout_5.addWidget(self.pushButton_HideUserPaths)


        self.verticalLayout_14.addWidget(self.frame_3)

        self.treeWidget_FoundFonts = QTreeWidget(self.frame_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Font Name");
        self.treeWidget_FoundFonts.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_FoundFonts.setObjectName(u"treeWidget_FoundFonts")
        self.treeWidget_FoundFonts.setMinimumSize(QSize(0, 80))

        self.verticalLayout_14.addWidget(self.treeWidget_FoundFonts)


        self.horizontalLayout_3.addWidget(self.frame_2)

        self.treeWidget_FontsInCategory = QTreeWidget(self.frame_ThirdRow)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"Font Name");
        self.treeWidget_FontsInCategory.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_FontsInCategory.setObjectName(u"treeWidget_FontsInCategory")
        sizePolicy1.setHeightForWidth(self.treeWidget_FontsInCategory.sizePolicy().hasHeightForWidth())
        self.treeWidget_FontsInCategory.setSizePolicy(sizePolicy1)
        self.treeWidget_FontsInCategory.setMaximumSize(QSize(220, 16777215))

        self.horizontalLayout_3.addWidget(self.treeWidget_FontsInCategory)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.frame_ThirdRow)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1075, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuMisc = QMenu(self.menubar)
        self.menuMisc.setObjectName(u"menuMisc")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMisc.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionTell_me_how)
        self.menuHelp.addAction(self.actionTips)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionTell_me_how.setText(QCoreApplication.translate("MainWindow", u"Tell me how", None))
        self.actionTips.setText(QCoreApplication.translate("MainWindow", u"Tips", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"System Paths (predefined)", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"User Paths", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Path Actions", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Add Path", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Remove Path", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Scan for Fonts", None))
        self.groupBox_RenderFrame.setTitle("")
        self.groupBox_RenderOptions.setTitle(QCoreApplication.translate("MainWindow", u"Render Options", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Render Text:", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"LCD Render", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Auto Hinting", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Use Kerning", None))
        self.pushButton_SelectColor.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.pushButton_ShowPaths.setText(QCoreApplication.translate("MainWindow", u"Show Paths", None))
        self.label_CurrentFont.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_CategoriesFrame.setTitle(QCoreApplication.translate("MainWindow", u"Categories", None))
        ___qtreewidgetitem = self.treeWidget_Categories.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Label", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Inst", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Icon", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Count", None));
        self.groupBox_CategoryActionsFrame.setTitle(QCoreApplication.translate("MainWindow", u"Category Actions", None))
        self.label_CategoryName.setText(QCoreApplication.translate("MainWindow", u"Enter Category Name:", None))
        self.pushButton_NewCategory.setText(QCoreApplication.translate("MainWindow", u"New Category", None))
        self.pushButton_DeleteCategory.setText(QCoreApplication.translate("MainWindow", u"Delete Category", None))
        self.pushButton_InsertFont.setText(QCoreApplication.translate("MainWindow", u"Insert Font\n"
"in Category", None))
        self.pushButton_RemoveFont.setText(QCoreApplication.translate("MainWindow", u"Remove Font \n"
"from Category", None))
        self.pushButton_InstallCategory.setText(QCoreApplication.translate("MainWindow", u"Install Category", None))
        self.pushButton_UninstallCategory.setText(QCoreApplication.translate("MainWindow", u"Uninstall Category", None))
        self.pushButton_UpdateSysCache.setText(QCoreApplication.translate("MainWindow", u"Update Sys Cache", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Search:", None))
        self.pushButton_ClearSearchText.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.pushButton_HideSysPaths.setText(QCoreApplication.translate("MainWindow", u"Hide Sys Paths", None))
        self.pushButton_HideUserPaths.setText(QCoreApplication.translate("MainWindow", u"Hide User Paths", None))
        ___qtreewidgetitem1 = self.treeWidget_FoundFonts.headerItem()
        ___qtreewidgetitem1.setText(7, QCoreApplication.translate("MainWindow", u"Id", None));
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("MainWindow", u"Font Path", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("MainWindow", u"License", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("MainWindow", u"Font Info", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("MainWindow", u"Font File", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("MainWindow", u"User Note", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"Font Style", None));
        ___qtreewidgetitem2 = self.treeWidget_FontsInCategory.headerItem()
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("MainWindow", u"Found it", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuMisc.setTitle(QCoreApplication.translate("MainWindow", u"Misc", None))
    # retranslateUi


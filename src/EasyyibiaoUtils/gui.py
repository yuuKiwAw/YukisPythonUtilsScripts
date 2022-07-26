import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QFileDialog, QMessageBox
from Ui_qtui import Ui_MainWindow
from EasyyibiaoDataFormat import EasyyiBiaoFormat


class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

        self.formatSelect_box.addItems(['base-json', 'yolo'])

        self.sourcePath_BTN.clicked.connect(self.selectSourcePath)
        self.savePath_BTN.clicked.connect(self.selectSavePath)
        self.format_BTN.clicked.connect(self.format_data)


    def selectSourcePath(self):
        directory = QFileDialog.getExistingDirectory(None,"select folder","C:/")  # 起始路径
        self.soureDir_txt.setText(directory)

    def selectSavePath(self):
        directory = QFileDialog.getExistingDirectory(None,"select folder","C:/")  # 起始路径
        self.saveDir_txt.setText(directory)


    def format_data(self):
        sourcePath = r"%s"%self.soureDir_txt.text()
        savePath = r"%s"%self.saveDir_txt.text()
        select_item = self.formatSelect_box.currentText()
        width = self.width_txt.text()
        height = self.height_txt.text()

        if sourcePath == "" or savePath == "":
            msg_box = QMessageBox(QMessageBox.Question, '退出', '请先选择路径')
            msg_box.exec_()
        else:
            easyyiBiaoFormat = EasyyiBiaoFormat(sourcePath, savePath)
            if select_item == 'base-json':
                easyyiBiaoFormat.ChangeDataFormat()
                msg_box = QMessageBox(QMessageBox.Question, '退出', '完成')
                msg_box.exec_()
            elif select_item == 'yolo':
                if width == '' or height == '':
                    msg_box = QMessageBox(QMessageBox.Question, '退出', '填写图片宽高')
                    msg_box.exec_()
                else:
                    easyyiBiaoFormat.ChangeDataFormatYolo([int(width), int(height)])
                    msg_box = QMessageBox(QMessageBox.Question, '退出', '完成')
                    msg_box.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())

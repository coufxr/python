import sys
from PyQt5.QtWidgets import QApplication, QWidget

def main():
    app = QApplication(sys.argv)

    w = QWidget()#窗口
    w.resize(450, 450)#尺寸大小
    w.move(800, 300)#位置
    w.setWindowTitle('标题')#标题
    w.show()#显示

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

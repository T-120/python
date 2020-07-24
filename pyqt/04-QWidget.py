# 0.导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1.创建一个应用程序对象
app = QApplication(sys.argv)

window = QWidget()

red = QWidget(window)
red.resize(100, 100)
red.setStyleSheet("background-color:red")

window.show()

# 3.应用程序的执行,进入到消息循环
sys.exit(app.exec())

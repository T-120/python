from PyQt5.Qt import *
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("车来！")
window.resize(500, 500)
window.move(400, 200)

label = QLabel(window)
label.setText("冲冲冲")
label.move(200, 200)

window.show()

sys.exit(app.exec())

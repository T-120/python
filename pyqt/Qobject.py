from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Qobject的学习")
        # self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        # self.QObject继承结构测试()
        # self.QObject对象名称和属性的操作()
        # self.QObject对象的父子关系操作()
        # self.QObject信号的操作()
        self.QObject类型的判定()
        # self.QObject对象删除()

    def QObject继承结构测试(self):
        # QObject.__subclasses__()
        mros = QObject.mro()
        for mro in mros:
            print(mro)

    def QObject对象名称和属性的操作(self):
        # 测试API
        # obj = QObject()
        # obj.setObjectName("notice")
        # print(obj.objectName())
        #
        # obj.setProperty("notice_level", "error")
        # obj.setProperty("notice_level2", "warning")
        #
        # print(obj.property("notice_level"))
        # print(obj.dynamicPropertyNames())

        # 案例演示
        with open("QObject.qss", "r") as f:
            qApp.setStyleSheet(f.read())

        label = QLabel(self)
        label.setObjectName("notice")
        label.setProperty("notice_level", "warning")
        label.setText("看我神威")

        label2 = QLabel(self)
        label2.move(100, 0)
        label2.setObjectName("notice")
        label2.setProperty("notice_level", "error")
        label2.setText("无坚不摧")

        label3 = QLabel(self)
        label3.move(200, 0)
        label3.setText("大威天龙")

        btn = QPushButton(self)
        btn.setObjectName("notice")
        btn.setText("PDD")
        btn.move(60, 30)
        # label.setStyleSheet("font-size:20px;color:red;")

    def QObject对象的父子关系操作(self):
        # 测试API---------------------------开始
        # obj0 = QObject()
        # obj1 = QObject()
        # obj2 = QObject()
        # obj3 = QObject()
        # obj4 = QObject()
        # obj5 = QObject()
        # print("obj0", obj0)
        # print("obj1", obj1)
        # print("obj2", obj2)
        # print("obj3", obj3)
        # print("obj4", obj4)
        # print("obj5", obj5)

        # obj1.setParent(obj0)
        # obj2.setParent(obj0)
        # obj2.setObjectName("2")
        # # label = QLabel()
        # # label.setParent(obj0)

        # obj3.setParent(obj1)
        # obj3.setObjectName("3")

        # obj4.setParent(obj2)
        # obj5.setParent(obj2)

        # print(obj1.parent())

        # print(obj0.children())

        # print(obj0.findChild(QObject, "3", Qt.FindDirectChildrenOnly))
        # print(obj0.findChildren(QObject))
        # 测试API---------------------------结束

        # ********************内存管理机制********************开始
        obj1 = QObject()
        self.obj1 = obj1
        obj2 = QObject()

        obj2.setParent(obj1)

        # 监听obj2对象被释放
        obj1.destroyed.connect(lambda: print("obj1对象被释放了"))
        obj2.destroyed.connect(lambda: print("obj2对象被释放了"))

        del self.obj1

        # ********************内存管理机制********************结束

    def QObject信号的操作(self):
        # self.obj = QObject()
        # 
        # # obj.destroyed()
        # # obj.objectNameChanged()
        # # def destroy_cao(obj):
        # #     print("对象被释放了", obj)
        # #
        # # self.obj.destroyed.connect(destroy_cao)
        # #
        # # del self.obj
        # 
        # def obj_name_cao(name):
        #     print("对象名称发生了改变", name)
        # 
        # def obj_name_cao2(name):
        #     print("对象名称发生了改变", name)
        # 
        # self.obj.objectNameChanged.connect(obj_name_cao)
        # self.obj.objectNameChanged.connect(obj_name_cao2)
        # 
        # # print(self.obj.receivers("objectNameChanged")) error
        # print(self.obj.receivers(self.obj.objectNameChanged))
        # self.obj.setObjectName("xxx")
        # 
        # # self.obj.objectNameChanged.disconnect()
        # # print(self.obj.signalsBlocked(), "1")
        # # self.obj.blockSignals(True)
        # #
        # # print(self.obj.signalsBlocked(), "2")
        # # self.obj.setObjectName("ooo")
        # #
        # # # self.obj.objectNameChanged.connect(obj_name_cao)
        # # self.obj.blockSignals(False)
        # # print(self.obj.signalsBlocked(), "3")
        # #
        # # self.obj.setObjectName("xxoo")

        # ********************信号与槽案例********************开始
        # btn = QPushButton(self)
        # btn.setText("点击我")
        #
        # def cao():
        #     print("大威天龙")
        #
        # btn.clicked.connect(cao)
        pass
        # ********************信号与槽案例********************结束

    def QObject类型的判定(self):
        # ********************API********************开始
        # obj = QObject()
        # w = QWidget()
        # btn = QPushButton()
        # label = QLabel()
        #
        # objs = [obj, w, btn, label]
        # for o in objs:
        #     # print(o.isWidgetType())
        #     # print(o.inherits("QWidget"))
        #     print(o.inherits("QPushButton"))
        # ********************API********************结束

        # ********************案例********************开始
        label1 = QLabel(self)
        label1.setText("看我神威")

        label2 = QLabel(self)
        label2.setText("无坚不摧")
        label2.move(60, 0)

        # del label2
        label2.deleteLater()

        btn = QPushButton(self)
        btn.setText("点我")
        btn.move(20, 20)

        # for widget in self.findChildren(QLabel):
        for widget in self.children():
            # print(widget)
            # if widget.isWidgetType():
            if widget.inherits("QLabel"):
                widget.setStyleSheet("background-color:cyan;")

        # ********************案例********************结束

    def QObject对象删除(self):
        obj1 = QObject()
        self.obj1 = obj1
        obj2 = QObject()
        obj3 = QObject()

        obj3.setParent(obj2)
        obj2.setParent(obj1)

        obj1.destroyed.connect(lambda: print("obj1被释放了"))
        obj2.destroyed.connect(lambda: print("obj2被释放了"))
        obj3.destroyed.connect(lambda: print("obj3被释放了"))

        # del obj2
        obj2.deleteLater()
        # print(obj1.children())
        print(obj2)
        # 才会真正的去释放相关的对象


def QWidget控件的父子关系(self):
    # win1 = QWidget()
    # win1.setWindowTitle("红色")
    # win1.setStyleSheet("background-color:red;")
    # win1.resize(500, 500)
    # win1.show()
    #
    # win2 = QWidget()
    # win2.setWindowTitle("蓝色")
    # win2.setStyleSheet("background-color:blue;")
    # # win2.setParent(win1)
    # win2.resize(1000, 100)
    # win2.show()

    win_root = QWidget()

    label1 = QLabel()
    label1.setText("Label1")
    label1.setParent(win_root)

    label2 = QLabel()
    label2.move(50, 50)
    label2.setText("Label2")
    label2.setParent(win_root)

    label3 = QLabel()
    label3.move(80, 80)
    label3.setText("Label3")
    label3.setParent(win_root)

    btn = QPushButton(win_root)
    btn.move(100, 100)
    btn.setText("btn")

    win_root.show()

    for sub_widget in win_root.findChildren(QLabel):
        sub_widget.setStyleSheet("background-color:cyan;")


def 信号与槽():
    # 连接窗口标题变化的信号 与 槽
    def cao(title):
        # print("窗口标题变化了", title)
        # window.windowTitleChanged.disconnect()
        window.blockSignals(True)
        window.setWindowTitle("py-" + title)
        window.blockSignals(False)
        # window.windowTitleChanged.connect(cao)

    window.windowTitleChanged.connect(cao)

    window.setWindowTitle("Hello Sz")
    window.setWindowTitle("Hello Sz2")
    window.setWindowTitle("Hello Sz3")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # QWidget控件的父子关系()
    window = Window()
    # window = QWidget()

    window.show()

    sys.exit(app.exec())

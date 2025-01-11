from interface import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionApp()
    window.show()
    sys.exit(app.exec_())